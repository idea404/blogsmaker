import json

from structlog import get_logger

from utils import DB_DIR

from .model import BlogSite

logger = get_logger()


class DBManager:
    def __init__(self, filename="db.json") -> None:
        self.file_path = DB_DIR / filename

    def _delete_db(self):
        logger.warning(f"Deleting db at {self.file_path}")
        if self.file_path.exists():
            self.file_path.unlink()

    def _load_db(self) -> dict:
        db = None
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                db = json.load(f)
        return db or {}

    def _save_db(self, data: dict):
        if not self.file_path.exists():
            with open(self.file_path, "x") as f:
                json.dump(data, f)
            return
        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def _get_site(self, subject: str) -> dict | None:
        db = self._load_db()
        return db.get(subject)

    def _set_site(self, subject: str, site: dict):
        db = self._load_db()
        db[subject] = site
        self._save_db(db)

    def get_blog_site(self, subject: str) -> BlogSite | None:
        status_dict = self._get_site(subject)
        if status_dict is None:
            return None
        return BlogSite(**status_dict)

    def save_blog_site(self, site: BlogSite):
        self._set_site(subject=site.subject, site=site.to_dict())

    def save_blog_sites(self, sites: list[BlogSite]):
        db = self._load_db()
        for site in sites:
            db[site.subject] = site.to_dict()
        self._save_db(db)

    def get_all_blog_sites(self) -> list[BlogSite]:
        db = self._load_db()
        return [BlogSite(**site) for site in db.values()]

    def delete_blog_site(self, subject: str):
        db = self._load_db()
        if subject in db:
            del db[subject]
        self._save_db(db)

    def get_or_create_blog_sites_from_subjects(
        self, subjects: list[str]
    ) -> list[BlogSite]:
        db = self._load_db()
        return [
            BlogSite(subject) if subject not in db else BlogSite(**db[subject])
            for subject in subjects
        ]
