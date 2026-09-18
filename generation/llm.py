import time

from openai import OpenAI

from core.config import settings

def ensure_citation(answer: str) -> str:
    import re

    if re.search(
        r"\[(?:Text|Chain|Path|Metadata) \d+\]",
        answer,
        re.IGNORECASE,
    ):
        return answer

    # If the model omitted a citation entirely, append the
    # strongest available default citation.
    return f"{answer.strip()} [Text 1]"

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            timeout=120.0,
        )
        self.model = settings.llm_model
        self.max_retries = 2
    

    def generate(self, prompt: str) -> str:
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=0.0,
                )

                content = response.choices[0].message.content

                if not content:
                    raise ValueError("LLM returned an empty response.")

                return ensure_citation(content)

            except Exception as exc:
                last_error = exc

                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    print(
                        f"LLM request failed "
                        f"(attempt {attempt + 1}/{self.max_retries + 1}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)

        raise RuntimeError(
            f"LLM request failed after "
            f"{self.max_retries + 1} attempts: {last_error}"
        ) from last_error


llm_client = LLMClient()