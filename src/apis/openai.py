import openai
import requests
from structlog import get_logger

from utils import OPENAI_API_KEY

logger = get_logger()


class OpenAIClient:
    def __init__(self) -> None:
        self.api_key = OPENAI_API_KEY
        assert openai.api_key, "OPENAI_API_KEY is not set"
        self.engine = "text-davinci-003"
        logger.debug("OpenAI client initialized")

    def list_engines(self):
        raise NotImplementedError()  # TODO

    def create_completion(
        self, prompt, max_tokens=100, temperature=0.9
    ) -> requests.Response:
        response = requests.post(
            url="https://api.openai.com/v1/completions",
            json={
                "prompt": prompt,
                "model": self.engine,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        return response
