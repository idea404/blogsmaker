from dataclasses import dataclass
import unsync
from structlog import get_logger

from apis.openai import OpenAIClient

logger = get_logger()

@dataclass
class SubjectDomain:
    subject: str
    domain: str

class BlogGenerator:
    def __init__(self) -> None:
        self.openai_client = OpenAIClient()
        logger.info("BlogGenerator initialized")

    def generate(self, subjects):
        logger.info(f"Generating blog sites for subjects: {subjects}")
        self.dns_search_and_register(subjects)

    def dns_search_and_register(self, subjects):
        subject_domains = self._dns_search(subjects)
        self._dns_register(subject_domains)

    def _dns_search(self, subjects) -> list[SubjectDomain]:
        logger.info(f"Searching for domains for subjects: {subjects}")
        tasks = [self._dns_search_subject(subject) for subject in subjects]
        return [task.result() for task in tasks]

    @unsync
    def _dns_search_subject(self, subject, max_attemps=10) -> SubjectDomain | None:
        logger.debug(f"Searching for domain for subject: {subject}")
        is_available_dns_found = False
        attempt = 0
        while not is_available_dns_found:
            attempt += 1
            domain = self._generate_domain(subject)
            is_available_dns_found = self._check_dns(domain)
            if attempt > max_attemps:
                logger.error(f"Max attempts reached for subject: {subject}")
                return 
        return SubjectDomain(subject, domain)
    
    def _generate_domain(self, subject) -> str:
        logger.debug(f"Generating domain for subject: {subject}")
        prompt = f"Generate a domain for subject {subject}"
        response = self.openai_client.create_completion(prompt)
        domain = response.choices[0].text.replace("\n\n", "")
        return domain
    
    def _check_dns(self, domain) -> bool:
        logger.debug(f"Checking DNS for domain: {domain}")
        # TODO: Implement DNS check using cloudflare API
        return True
