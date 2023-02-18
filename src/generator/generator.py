import unsync
from structlog import get_logger

from apis.openai import OpenAIClient
from db import BlogSite, DBManager

logger = get_logger()

class BlogGenerator:
    def __init__(self) -> None:
        self.openai_client = OpenAIClient()
        logger.info("BlogGenerator initialized")

    def generate(self, subjects: list[str]):
        logger.info(f"Generating blog sites for subjects: {subjects}")
        sites = self._instantiate_blog_sites(subjects)
        sites = self.dns_search_and_register(sites)

    def _instantiate_blog_sites(self, subjects: list[str]) -> list[BlogSite]:
        logger.info(f"Instantiating blog sites for subjects: {subjects}")
        sites = []
        for subject in subjects:
            site_status = DBManager.get_blog_site_status(subject)
            if site_status is None:
                site_status = BlogSite(subject)
                DBManager.set_blog_site_status(site_status)
            sites.append(site_status)
        return sites

    def dns_search_and_register(self, site_statuses: list[BlogSite]) -> list[BlogSite]:
        sites = self._dns_search(site_statuses)
        sites = self._dns_register(site_statuses)
        return sites

    def _dns_search(self, site_statuses: list[BlogSite]) -> list[BlogSite]:
        domainless_sites = [site for site in site_statuses if site.domain is None]
        logger.info(f"Searching for domains for subjects: {domainless_sites}")
        tasks = [self._dns_search_subject(site) for site in domainless_sites]
        return [task.result() for task in tasks]

    @unsync
    def _dns_search_subject(self, site: BlogSite, max_attemps=10) -> BlogSite:
        logger.debug(f"Searching for domain for site: {site}")
        is_available_dns = False
        attempt = 0
        while not is_available_dns:
            attempt += 1
            domain = self._generate_new_domain(site)
            site.desired_domains.add(domain)
            is_available_dns = self._check_dns_availability(domain)
            if attempt > max_attemps:
                logger.error(f"Max attempts DNS search reached for site: {site}")
                return 
        site.available_domain = domain
        return site

    def _generate_new_domain(self, site: BlogSite) -> str:
        logger.debug(f"Asking openAI for domain for site: {site}")
        prompt = f"Generate a domain for subject {site.subject}"
        # TODO: Use whitelist for domain suffixes
        # TODO: Use site.desited_domains to avoid duplicates
        response = self.openai_client.create_completion(prompt)
        domain = response.choices[0].text.replace("\n\n", "")
        return domain
    
    def _check_dns_availability(self, domain: str) -> bool:
        logger.debug(f"Checking DNS for domain: {domain}")
        # TODO: Implement DNS check using cloudflare API
        return True
