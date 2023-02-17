import os

import openai
from structlog import get_logger

logger = get_logger()

class OpenAIClient: 
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        assert openai.api_key, "OPENAI_API_KEY is not set"
        self.engine = "text-davinci-003"
        logger.debug("OpenAI client initialized")

    def list_engines(self):
        return openai.Engine.list()
    
    def create_completion(self, prompt, max_tokens=100, temperature=0.9):
        response = openai.Completion.create(
            model=self.engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response


if __name__ == "__main__":
    client = OpenAIClient()
    prompt = "Tell me a story about a cat"
    response = client.create_completion(prompt)
    print(response)
