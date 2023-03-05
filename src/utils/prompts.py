class BlogSiteGenerationPrompts:
    @staticmethod
    def domain_prompt(subject: str) -> str:
        return f"""
          Generate a domain for the subject: {subject}.
        """

    @staticmethod
    def site_article_topic_list_prompt(subject: str, n_subtopics: int) -> str:
        return f"""
          Generate a list of {n_subtopics} subtopics for the subject: {subject}.
          Provide this list on a single line and separate each subtopic with a comma.
        """

    @staticmethod
    def site_article_text_prompt(subject: str, topic: str, n_words: int) -> str:
        return f"""
          Write an article of approximately {n_words} words about {topic} within the subject of {subject}. 
          Mark titles as, "Title: " followed by the title, and similarly for subtitles, "Subtitle: " followed by the subtitle. 
          Mark the end of the article with "End of article.".
        """
