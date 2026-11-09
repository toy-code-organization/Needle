from pathlib import Path


def read_text_document(file_path: Path) -> str:
    if not file_path.is_file():
        raise FileNotFoundError(f"문서 파일을 찾을 수 없습니다: {file_path}")

    if file_path.suffix.lower() != ".txt":
        raise ValueError(f"지원하지 않는 파일 형식입니다: {file_path.suffix}")

    content = file_path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError("문서 내용이 비어 있습니다.")

    return content
