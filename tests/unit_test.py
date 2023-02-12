from unittest import TestCase

from src.cli.cli import CommandLineInterface

class Test(TestCase):
    def test_initialize_cli(self):
        CommandLineInterface()
