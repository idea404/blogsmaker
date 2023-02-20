import time


class MockOpenAIClient:
    def __init__(self, **kwargs):
        pass

    def create_completion(self, prompt) -> str:
        time.sleep(0.5)
        if "Generate a domain" in prompt:
            return "example.com"
        return ""


class MockCloudflareClient:
    pass
