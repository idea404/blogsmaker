import random

from structlog import get_logger
from unsync import unsync

from apis import OpenAIClient
from db import BlogSite, BlogSiteArticle
from utils import (
    MAX_N_ARTICLES,
    MAX_N_WORDS,
    MIN_N_ARTICLES,
    MIN_N_WORDS,
    BlogSiteGenerationPrompts,
)

logger = get_logger()


class OpenAIManager:
    def __init__(self, openai_client: OpenAIClient) -> None:
        logger.info("OpenAIManager initialized")
        self.openai_client = openai_client

    def generate_sites_article_topics(self, sites: list[BlogSite]) -> list[BlogSite]:
        logger.info(f"Generating content for {len(sites)} sites")
        tasks = [self._generate_site_content(site) for site in sites]
        return [task.result() for task in tasks]  # type: ignore

    @unsync
    def _generate_site_content(
        self,
        site: BlogSite,
        min_n_articles: int = MIN_N_ARTICLES,
        max_n_articles: int = MAX_N_ARTICLES,
        min_n_words: int = MIN_N_WORDS,
        max_n_words: int = MAX_N_WORDS,
    ) -> BlogSite:
        logger.debug(f"Generating content for site: {site}")
        if site.articles:
            logger.debug(f"Site already has articles: {site}")
            return site
        n_articles = random.randint(min_n_articles, max_n_articles)
        site_articles = self._request_article_topics(site.subject, n_articles)
        site.articles = site_articles
        for article in site.articles:
            n_words = random.randint(min_n_words, max_n_words)
            article_content_text_string = self._request_article_text(
                site.subject, article.topic, n_words
            )
            article.content = article_content_text_string

        return site

    def _request_article_topics(
        self, subject: str, n_topics: int
    ) -> list[BlogSiteArticle]:
        logger.debug(f"Requesting subtopics for subject: {subject}")
        prompt = BlogSiteGenerationPrompts.site_article_topic_list_prompt(
            subject, n_topics
        )
        topics_string = self.openai_client.create_completion(prompt)
        topics = self._parse_topics_string(topics_string)
        return [BlogSiteArticle(topic) for topic in topics]

    def _request_article_text(self, subject: str, topic: str, n_words: int) -> str:
        logger.debug(
            f"Requesting article text for subject {subject} with topic {topic} in {n_words} words"
        )
        prompt = BlogSiteGenerationPrompts.site_article_text_prompt(
            subject, topic, n_words
        )
        article_text = self.openai_client.create_completion(prompt)
        article_text = self._parse_article_text_string(article_text)
        return article_text

    def _parse_topics_string(self, topics_string: str) -> list[str]:
        logger.debug(f"Parsing topics string: {str(topics_string)}")
        split_list = topics_string.split(", ")
        topics = [topic.replace("\n", "").strip() for topic in split_list]
        return topics

    def _parse_article_text_string(self, article_text_string: str) -> str:
        logger.debug(
            f"Parsing article text string of length {len(article_text_string)}"
        )
        article_text = article_text_string.strip()
        return article_text
