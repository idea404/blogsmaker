from unittest import TestCase

from apis import OpenAIClient


class TestIntegrationTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = OpenAIClient()

    def tearDown(self) -> None:
        super().tearDown()
        self.client = None

    def test_openai_client(self):
        prompt = "Say this in Dutch: Monday"
        response = self.client.create_completion(prompt, temperature=0)
        self.assertTrue(response)
        response_text = response.json()["choices"][0]["text"].replace("\n\n", "")
        self.assertEquals(response_text, "Maandag")
