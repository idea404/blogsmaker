import json

from model import BlogSite


class DBManager: 
    file = "status.json"

    @staticmethod
    def _load_db() -> dict:
        with open(DBManager.file, "r") as f:
            return json.load(f)
        
    @staticmethod
    def _save_db(data: dict):
        with open(DBManager.file, "w") as f:
            json.dump(data, f)
    
    @staticmethod
    def _get_status(subject: str) -> dict | None:
        db = DBManager._load_db()
        return db.get(subject)

    @staticmethod
    def _set_status(subject: str, status: dict):
        db = DBManager._load_db()
        db[subject] = status
        DBManager._save_db(db)

    @staticmethod
    def get_blog_site_status(status: str) -> BlogSite | None:
        status_dict = DBManager._get_status(status)
        if status_dict is None:
            return None
        return BlogSite(**status_dict)

    @staticmethod
    def set_blog_site_status(status: BlogSite):
        DBManager._set_status(status.subject, status.to_dict())