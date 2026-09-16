import httpx

from core.config import settings


class LLMClient:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model = settings.llm_model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        response = httpx.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": 0.2,
            },
            timeout=60.0,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Groq API error {response.status_code}: {response.text}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]


llm_client = LLMClient()