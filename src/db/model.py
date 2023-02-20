from dataclasses import dataclass, field


@dataclass
class BlogSite:
    subject: str
    available_domain: str = None
    desired_domains: dict = field(default_factory=dict)
    registered_domain: str = None

    def to_dict(self) -> dict:
        return self.__dict__
