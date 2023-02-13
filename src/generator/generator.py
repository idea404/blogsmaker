from structlog import get_logger

logger = get_logger()

class BlogGenerator:
    def __init__(self) -> None:
        logger.info("BlogGenerator initialized")

    def generate(self, subjects):
        logger.info(f"Generating blog posts for subjects: {subjects}")