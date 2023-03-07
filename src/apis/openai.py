import requests
from structlog import get_logger

from utils import GPT3_ENGINE, GPT3_URL, OPENAI_API_KEY

logger = get_logger()


class OpenAIClient:
    def __init__(
        self,
        api_key: str | None = OPENAI_API_KEY,
        engine: str | None = GPT3_ENGINE,
        gpt3_url: str | None = GPT3_URL,
    ) -> None:
        assert gpt3_url, "GPT3_URL is not set"
        assert api_key, "OPENAI_API_KEY is not set"
        assert engine, "GPT3_ENGINE is not set"
        self.api_key: str = api_key
        self.engine: str = engine
        self.gpt3_url: str = gpt3_url
        logger.debug("OpenAI client initialized")

    def list_engines(self):
        raise NotImplementedError()  # TODO

    def _request_create_completion(
        self, prompt: str, max_tokens: int = 100, temperature: float = 0.9
    ) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        json_data = {
            "model": self.engine,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }
        logger.debug("OpenAI request", request=json_data)
        response = requests.post(url=self.gpt3_url, json=json_data, headers=headers)

        return response

    def create_completion(
        self, prompt: str, max_tokens: int = 2800, temperature: float = 0.9
    ) -> str:
        response = self._request_create_completion(
            prompt, max_tokens=max_tokens, temperature=temperature
        )
        response.raise_for_status()

        if "error" in response.json():
            logger.error("OpenAI error", error=response.json()["error"])
            raise RuntimeError(response.json()["error"])

        logger.debug("OpenAI response", response=response.json())
        return response.json()["choices"][0]["message"]["content"]
