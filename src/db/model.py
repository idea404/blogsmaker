from dataclasses import dataclass


@dataclass
class BlogSite:
    subject: str
    available_domain: str = None
    desired_domains: set = set()
    registered_domain: str = None

    def to_dict(self) -> dict:
        return self.__dict__