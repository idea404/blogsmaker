from unittest import TestCase


class TestIntegrationTests(TestCase):
    def test_openai_client(self):
        from src.apis.openai import OpenAIClient

        client = OpenAIClient()
        prompt = "Say this in Dutch: Monday"
        response = client.create_completion(prompt)
        self.assertTrue(response)
        response_text = response.choices[0].text.replace("\n\n", "")
        self.assertEquals(response_text, "Maandag")