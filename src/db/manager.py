import json

from structlog import get_logger

from utils import DB_DIR

from .model import BlogSite

logger = get_logger()


class DBManager:
    def __init__(self, filename="status.json") -> None:
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

    def _set_site(self, subject: str, status: dict):
        db = self._load_db()
        db[subject] = status
        self._save_db(db)

    def get_blog_site(self, status: str) -> BlogSite | None:
        status_dict = self._get_site(status)
        if status_dict is None:
            return None
        return BlogSite(**status_dict)

    def save_blog_site(self, status: BlogSite):
        self._set_site(subject=status.subject, status=status.to_dict())
