from dataclasses import asdict, dataclass, field


@dataclass
class BlogSiteArticle:
    topic: str
    content: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BlogSite:
    subject: str
    available_domain: str | None = None
    desired_domains: dict = field(default_factory=dict)
    registered_domain: str | None = None
    articles: list[BlogSiteArticle] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
