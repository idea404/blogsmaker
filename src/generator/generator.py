import random

from structlog import get_logger
from unsync import unsync

from apis import CloudflareClient, OpenAIClient
from db import BlogSite, BlogSiteArticle, DBManager
from utils import BlogSiteGenerationPrompts

logger = get_logger()


class BlogGenerator:
    def __init__(self) -> None:
        openai_client = OpenAIClient()
        self.db = DBManager()
        self.openai_manager = OpenAIManager(openai_client)
        self.dns_manager = DNSManager(openai_client, CloudflareClient())
        logger.info("BlogGenerator initialized")

    def generate(self, subjects: list[str]):
        logger.info(f"Generating blog sites for subjects: {subjects}")
        sites = self._instantiate_blog_sites(subjects)
        sites = self.dns_manager.search_and_register(sites)
        sites = self.openai_manager.generate_sites_article_topics(sites)

    def _instantiate_blog_sites(self, subjects: list[str]) -> list[BlogSite]:
        logger.info(f"Instantiating blog sites for subjects: {subjects}")
        sites = []
        for subject in subjects:
            site = self.db.get_blog_site(subject)
            if not site:
                site = BlogSite(subject)
                self.db.save_blog_site(site)
            sites.append(site)
        return sites


class DNSManager:
    def __init__(self, openai_client: OpenAIClient, cloudflare_client) -> None:
        logger.info("DNSManager initialized")
        self.openai_client = openai_client
        self.cloudflare_client = cloudflare_client

    def search_and_register(self, site_statuses: list[BlogSite]) -> list[BlogSite]:
        sites = self._search(site_statuses)
        sites = self._dns_register(site_statuses)
        return sites

    def _search(self, sites: list[BlogSite]) -> list[BlogSite]:
        logger.info(f"Searching for domains for {len(sites)} subjects")
        tasks = [self._search_subject(site) for site in sites]
        return [task.result() for task in tasks]  # type: ignore

    @unsync
    def _search_subject(self, site: BlogSite, max_attempts=10) -> BlogSite:
        logger.debug(f"Searching for domain for site: {site}")
        if site.available_domain:
            logger.debug(f"Site already has available domain: {site}")
            return site

        is_available_dns = False
        attempt = 0
        domain = None
        while not is_available_dns:
            attempt += 1
            domain = self._generate_new_domain(site)
            site.desired_domains[domain] = "unverified"
            is_available_dns = self._check_availability(domain)
            site.desired_domains[domain] = "verified"
            if attempt > max_attempts:
                logger.error(f"Max attempts DNS search reached for site: {site}")
                return site
        site.available_domain = domain

        return site

    def _generate_new_domain(self, site: BlogSite) -> str:
        logger.debug(f"Asking openAI for domain for site: {site}")
        prompt = BlogSiteGenerationPrompts.domain_prompt(site.subject)
        # TODO: Use whitelist for domain suffixes
        # TODO: Use site.desired_domains to avoid duplicates
        domain = self.openai_client.create_completion(prompt)
        return domain

    def _check_availability(self, domain: str) -> bool:
        logger.debug(f"Checking DNS for domain: {domain}")
        # TODO: Implement DNS check using cloudflare API
        # TODO: Implement price check using DNSimple API
        return True


class OpenAIManager:
    def __init__(self, openai_client: OpenAIClient) -> None:
        logger.info("OpenAIManager initialized")
        self.openai_client = openai_client

    def generate_sites_article_topics(self, sites: list[BlogSite]) -> list[BlogSite]:
        logger.info(f"Generating content for {len(sites)} sites")
        tasks = [self._generate_site_content(site) for site in sites]
        return [task.result() for task in tasks]  # type: ignore

    @unsync
    def _generate_site_content(self, site: BlogSite) -> BlogSite:
        logger.debug(f"Generating content for site: {site}")
        if site.articles:
            logger.debug(f"Site already has articles: {site}")
            return site
        n_articles = random.randint(7, 13)
        topics_list = self._request_article_topics(site.subject, n_articles)
        site.articles = topics_list
        for article in site.articles:
            n_words = random.randint(700, 1900)
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
