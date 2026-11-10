from collections.abc import Iterator
from dataclasses import dataclass

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


@dataclass(frozen=True)
class DocumentChunk:
    chunk_order: int
    chunk_text: str


def chunk_document(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> Iterator[DocumentChunk]:
    if not text or text.isspace():
        raise ValueError("문서 내용이 비어 있습니다.")
    if chunk_size <= 0:
        raise ValueError("청크 크기는 0보다 커야 합니다.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("오버랩은 0 이상이며 청크 크기보다 작아야 합니다.")

    start = 0
    chunk_order = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        yield DocumentChunk(
            chunk_order=chunk_order,
            chunk_text=text[start:end],
        )

        if end == len(text):
            break

        start = end - overlap
        chunk_order += 1
