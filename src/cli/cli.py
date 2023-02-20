from structlog import get_logger

from generator import BlogGenerator

logger = get_logger()


class CommandLineInterface:
    def __init__(self):
        self.generator = BlogGenerator()
        logger.info("CLI initialized")

    def start(self):
        val = input("Pass subjects separated by comma: \n")
        subjects = [x.strip() for x in val.split(",")]
        self.generator.generate(subjects)
