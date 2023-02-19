from unittest import TestCase

from db import DBManager, BlogSite


class TestIntegrationTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.db = DBManager("test_status.json")

    def tearDown(self) -> None:
        super().tearDown()
        self.db._delete_db()
        self.db = None

    def test_db_save(self):
        site = BlogSite("test")
        self.db.save_blog_site(site)
        site = self.db.get_blog_site("test")
        self.assertEqual(site.subject, "test")

    def test_db_save_and_update(self):
        site = BlogSite("test")
        self.db.save_blog_site(site)
        site = self.db.get_blog_site("test")
        self.assertEqual(site.subject, "test")
        site.available_domain = "test.com"
        site.desired_domains = {"test.com": "unverified", "test.nl": "verified"}
        self.db.save_blog_site(site)
        site = self.db.get_blog_site("test")
        self.assertEqual(site.subject, "test")
        self.assertEqual(site.available_domain, "test.com")
        self.assertEqual(site.desired_domains, {"test.com": "unverified", "test.nl": "verified"})
