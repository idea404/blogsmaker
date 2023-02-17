from unittest import TestCase

from src.cli.cli import CommandLineInterface

class TestUnitTests(TestCase):
    def test_initialize_cli(self):
        CommandLineInterface()
