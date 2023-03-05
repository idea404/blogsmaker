from structlog import get_logger
from unsync import unsync

from apis import CloudflareClient, OpenAIClient
from db import BlogSite
from utils import MAX_DOMAIN_SEARCH_ATTEMPTS, BlogSiteGenerationPrompts

logger = get_logger()


class DNSManager:
    def __init__(
        self, openai_client: OpenAIClient, cloudflare_client: CloudflareClient
    ) -> None:
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
    def _search_subject(
        self, site: BlogSite, max_attempts: int = MAX_DOMAIN_SEARCH_ATTEMPTS
    ) -> BlogSite:
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
