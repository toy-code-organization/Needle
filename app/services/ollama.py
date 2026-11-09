import os

import httpx


class OllamaClient:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    @classmethod
    def from_environment(cls) -> "OllamaClient":
        return cls(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b"),
        )

    async def generate(self, question: str) -> str:
        payload = {
            "model": self.model,
            "prompt": question,
            "stream": False,
            "think": False,
            "options": {"temperature": 0, "num_predict": 128},
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()

        answer = response.json().get("response", "").strip()
        if not answer:
            raise RuntimeError("Ollama returned an empty response")
        return answer
