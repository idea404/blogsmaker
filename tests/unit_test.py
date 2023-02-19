from unittest import TestCase

from cli import CommandLineInterface

class TestUnitTests(TestCase):
    def test_initialize_cli(self):
        CommandLineInterface()
