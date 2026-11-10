import unittest
from math import inf, nan
from unittest.mock import AsyncMock, Mock, patch

import httpx

from app.services.embedding import EmbeddingClient


class EmbeddingClientTests(unittest.IsolatedAsyncioTestCase):
    def test_creates_client_from_environment(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "OLLAMA_BASE_URL": "http://host.docker.internal:11434/",
                "OLLAMA_EMBEDDING_MODEL": "bge-m3:latest",
            },
            clear=True,
        ):
            client = EmbeddingClient.from_environment()

        self.assertEqual(client.base_url, "http://host.docker.internal:11434")
        self.assertEqual(client.model, "bge-m3:latest")

    def test_uses_defaults_when_environment_is_missing(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            client = EmbeddingClient.from_environment()

        self.assertEqual(client.base_url, "http://localhost:11434")
        self.assertEqual(client.model, "bge-m3:latest")

    async def test_returns_embedding(self) -> None:
        response = Mock()
        response.json.return_value = {
            "embeddings": [[0.1, -0.2, 0.3]],
        }

        with patch("app.services.embedding.httpx.AsyncClient") as client_class:
            http_client = AsyncMock()
            client_class.return_value.__aenter__.return_value = http_client
            http_client.post.return_value = response

            client = EmbeddingClient(
                base_url="http://ollama:11434/",
                model="bge-m3:latest",
            )
            embedding = await client.embed("연차는 15일입니다.")

        self.assertEqual(embedding, [0.1, -0.2, 0.3])
        http_client.post.assert_awaited_once_with(
            "http://ollama:11434/api/embed",
            json={
                "model": "bge-m3:latest",
                "input": "연차는 15일입니다.",
                "truncate": True,
            },
        )
        response.raise_for_status.assert_called_once_with()

    async def test_raises_when_text_is_empty(self) -> None:
        client = EmbeddingClient(
            base_url="http://ollama:11434",
            model="bge-m3:latest",
        )

        for text in ("", "   ", "\n\t"):
            with self.subTest(text=repr(text)):
                with self.assertRaises(ValueError):
                    await client.embed(text)

    async def test_raises_when_response_has_no_embedding(self) -> None:
        for response_data in ({}, {"embeddings": None}, {"embeddings": []}):
            with self.subTest(response_data=response_data):
                response = Mock()
                response.json.return_value = response_data

                with patch(
                    "app.services.embedding.httpx.AsyncClient"
                ) as client_class:
                    http_client = AsyncMock()
                    client_class.return_value.__aenter__.return_value = http_client
                    http_client.post.return_value = response

                    client = EmbeddingClient(
                        base_url="http://ollama:11434",
                        model="bge-m3:latest",
                    )

                    with self.assertRaises(RuntimeError):
                        await client.embed("문서 내용")

    async def test_raises_when_response_is_not_an_object(self) -> None:
        response = Mock()
        response.json.return_value = []

        with patch("app.services.embedding.httpx.AsyncClient") as client_class:
            http_client = AsyncMock()
            client_class.return_value.__aenter__.return_value = http_client
            http_client.post.return_value = response

            client = EmbeddingClient(
                base_url="http://ollama:11434",
                model="bge-m3:latest",
            )

            with self.assertRaises(RuntimeError):
                await client.embed("문서 내용")

    async def test_raises_when_embedding_is_empty_or_not_a_list(self) -> None:
        for embedding in ([], "잘못된 값"):
            with self.subTest(embedding=embedding):
                response = Mock()
                response.json.return_value = {"embeddings": [embedding]}

                with patch(
                    "app.services.embedding.httpx.AsyncClient"
                ) as client_class:
                    http_client = AsyncMock()
                    client_class.return_value.__aenter__.return_value = http_client
                    http_client.post.return_value = response

                    client = EmbeddingClient(
                        base_url="http://ollama:11434",
                        model="bge-m3:latest",
                    )

                    with self.assertRaises(RuntimeError):
                        await client.embed("문서 내용")

    async def test_raises_when_embedding_contains_invalid_number(self) -> None:
        for value in ("잘못된 값", True, nan, inf):
            with self.subTest(value=value):
                response = Mock()
                response.json.return_value = {
                    "embeddings": [[0.1, value]],
                }

                with patch(
                    "app.services.embedding.httpx.AsyncClient"
                ) as client_class:
                    http_client = AsyncMock()
                    client_class.return_value.__aenter__.return_value = http_client
                    http_client.post.return_value = response

                    client = EmbeddingClient(
                        base_url="http://ollama:11434",
                        model="bge-m3:latest",
                    )

                    with self.assertRaises(RuntimeError):
                        await client.embed("문서 내용")

    async def test_propagates_ollama_http_error(self) -> None:
        response = Mock()
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Ollama 요청 실패",
            request=httpx.Request("POST", "http://ollama:11434/api/embed"),
            response=httpx.Response(500),
        )

        with patch("app.services.embedding.httpx.AsyncClient") as client_class:
            http_client = AsyncMock()
            client_class.return_value.__aenter__.return_value = http_client
            http_client.post.return_value = response

            client = EmbeddingClient(
                base_url="http://ollama:11434",
                model="bge-m3:latest",
            )

            with self.assertRaises(httpx.HTTPStatusError):
                await client.embed("문서 내용")

    async def test_propagates_ollama_connection_error(self) -> None:
        with patch("app.services.embedding.httpx.AsyncClient") as client_class:
            http_client = AsyncMock()
            client_class.return_value.__aenter__.return_value = http_client
            http_client.post.side_effect = httpx.ConnectError("Ollama 연결 실패")

            client = EmbeddingClient(
                base_url="http://ollama:11434",
                model="bge-m3:latest",
            )

            with self.assertRaises(httpx.ConnectError):
                await client.embed("문서 내용")


if __name__ == "__main__":
    unittest.main()
