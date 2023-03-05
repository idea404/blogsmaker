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
