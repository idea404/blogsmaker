from structlog import get_logger

from apis import CloudflareClient, OpenAIClient
from db import BlogSite, DBManager
from manager import DNSManager, OpenAIManager

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
        sites = self.db.get_or_create_blog_sites_from_subjects(subjects)
        self.db.save_blog_sites(sites)
        sites = self.dns_manager.search_and_register(sites)
        self.db.save_blog_sites(sites)
        sites = self.openai_manager.generate_sites_article_topics(sites)
        self.db.save_blog_sites(sites)
