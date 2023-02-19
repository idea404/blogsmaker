from unittest import TestCase

from db import DBManager, BlogSite


class TestIntegrationTests(TestCase):
    def test_db_save(self):
        db = DBManager()
        site = BlogSite("test")
        db.save_blog_site(site)
        site = db.get_blog_site("test")
        self.assertEqual(site.subject, "test")
