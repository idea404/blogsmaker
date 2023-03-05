import time
from unittest import TestCase

from cli import CommandLineInterface
from db import BlogSite
from manager import DNSManager
from tests.mocks import MockCloudflareClient, MockOpenAIClient


class TestUnitTests(TestCase):
    def test_initialize_cli(self):
        CommandLineInterface()

    def test_dns_manager(self):
        dns_manager = DNSManager(
            openai_client=MockOpenAIClient(),  # type: ignore
            cloudflare_client=MockCloudflareClient(),  # type: ignore
        )
        self.assertTrue(dns_manager)
        sites = [
            BlogSite("test1"),
            BlogSite("test2"),
            BlogSite("test3"),
            BlogSite("test4"),
            BlogSite("test5"),
        ]
        start_time = time.time()
        returned_sites = dns_manager._search(sites)
        end_time = time.time()
        expected_sites = [
            BlogSite("test1", "example.com", {"example.com": "verified"}),
            BlogSite("test2", "example.com", {"example.com": "verified"}),
            BlogSite("test3", "example.com", {"example.com": "verified"}),
            BlogSite("test4", "example.com", {"example.com": "verified"}),
            BlogSite("test5", "example.com", {"example.com": "verified"}),
        ]
        self.assertTrue(end_time - start_time < 2.5)
        self.assertEqual(returned_sites, expected_sites)
