import os
from math import isfinite

import httpx


class EmbeddingClient:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    @classmethod
    def from_environment(cls) -> "EmbeddingClient":
        return cls(
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            ),
            model=os.getenv(
                "OLLAMA_EMBEDDING_MODEL",
                "bge-m3:latest",
            ),
        )

    async def embed(self, text: str) -> list[float]:
        if not text or text.isspace():
            raise ValueError("임베딩할 문서 내용이 비어 있습니다.")

        payload = {
            "model": self.model,
            "input": text,
            "truncate": True,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/embed",
                json=payload,
            )
            response.raise_for_status()

        response_data = response.json()

        if not isinstance(response_data, dict):
            raise RuntimeError("Ollama 임베딩 응답 형식이 잘못되었습니다.")

        embeddings = response_data.get("embeddings")

        if not isinstance(embeddings, list) or len(embeddings) != 1:
            raise RuntimeError("Ollama 임베딩 응답 형식이 잘못되었습니다.")

        embedding = embeddings[0]

        if not isinstance(embedding, list) or not embedding:
            raise RuntimeError("Ollama가 빈 임베딩을 반환했습니다.")

        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and isfinite(float(value))
            for value in embedding
        ):
            raise RuntimeError("임베딩에 유효하지 않은 숫자가 포함되어 있습니다.")

        return [float(value) for value in embedding]
