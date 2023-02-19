import json
import os

from .model import BlogSite


class DBManager:
    def __init__(self, file=None) -> None:
        self.file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "db", "status.json"
        )

    def _load_db(self) -> dict:
        with open(DBManager.file_path, "r") as f:
            return json.load(f)

    def _save_db(self, data: dict):
        with open(DBManager.file_path, "w") as f:
            json.dump(data, f)

    def _get_site(self, subject: str) -> dict | None:
        db = DBManager._load_db()
        return db.get(subject)

    def _set_site(self, subject: str, status: dict):
        db = DBManager._load_db()
        db[subject] = status
        DBManager._save_db(db)

    def get_blog_site(self, status: str) -> BlogSite | None:
        status_dict = DBManager._get_site(status)
        if status_dict is None:
            return None
        return BlogSite(**status_dict)

    def save_blog_site(self, status: BlogSite):
        DBManager._set_site(status.subject, status.to_dict())
