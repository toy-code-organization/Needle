import unittest

from app.services.document_chunker import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    chunk_document,
)


class ChunkDocumentTests(unittest.TestCase):
    def test_returns_one_chunk_when_text_is_shorter_than_chunk_size(self) -> None:
        text = "가" * 500

        chunks = list(chunk_document(text))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].chunk_order, 0)
        self.assertEqual(chunks[0].chunk_text, text)

    def test_returns_one_chunk_when_text_matches_chunk_size(self) -> None:
        text = "가" * CHUNK_SIZE

        chunks = list(chunk_document(text))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].chunk_text, text)

    def test_returns_multiple_chunks_when_text_exceeds_chunk_size(self) -> None:
        text = "가" * 1500

        chunks = list(chunk_document(text))

        self.assertEqual(len(chunks), 3)
        self.assertEqual(
            [len(chunk.chunk_text) for chunk in chunks],
            [800, 800, 140],
        )

    def test_overlaps_adjacent_chunks_by_configured_length(self) -> None:
        text = "".join(str(index % 10) for index in range(1500))

        chunks = list(chunk_document(text))

        for current, following in zip(chunks, chunks[1:]):
            self.assertEqual(
                current.chunk_text[-CHUNK_OVERLAP:],
                following.chunk_text[:CHUNK_OVERLAP],
            )

    def test_preserves_chunk_order(self) -> None:
        chunks = list(chunk_document("가" * 1500))

        self.assertEqual(
            [chunk.chunk_order for chunk in chunks],
            [0, 1, 2],
        )

    def test_uses_custom_chunk_settings(self) -> None:
        chunks = list(chunk_document("abcdefghij", chunk_size=6, overlap=2))
        chunks_without_overlap = list(
            chunk_document("abcdefghij", chunk_size=6, overlap=0)
        )

        self.assertEqual(
            [chunk.chunk_text for chunk in chunks],
            ["abcdef", "efghij"],
        )
        self.assertEqual(
            [chunk.chunk_text for chunk in chunks_without_overlap],
            ["abcdef", "ghij"],
        )

    def test_raises_when_text_is_empty_or_whitespace(self) -> None:
        for text in ("", "   ", "\n\t"):
            with self.subTest(text=repr(text)):
                with self.assertRaises(ValueError):
                    list(chunk_document(text))

    def test_raises_when_chunk_settings_are_invalid(self) -> None:
        invalid_settings = (
            {"chunk_size": 0},
            {"overlap": -1},
            {"chunk_size": 120, "overlap": 120},
            {"chunk_size": 120, "overlap": 121},
        )

        for settings in invalid_settings:
            with self.subTest(settings=settings):
                with self.assertRaises(ValueError):
                    list(chunk_document("문서 내용", **settings))


if __name__ == "__main__":
    unittest.main()
