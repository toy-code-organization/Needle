import tempfile
import unittest
from pathlib import Path

from app.services.document_reader import read_text_document


class ReadTextDocumentTests(unittest.TestCase):
    def test_reads_utf8_text_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            file_path = Path(temp_directory) / "sample.txt"
            expected = "배포 전 동료 검토를 진행한다."
            file_path.write_text(expected, encoding="utf-8")

            actual = read_text_document(file_path)

            self.assertEqual(actual, expected)

    def test_raises_when_file_does_not_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            missing_file = Path(temp_directory) / "missing.txt"

            with self.assertRaises(FileNotFoundError):
                read_text_document(missing_file)

    def test_raises_when_file_is_not_txt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            markdown_file = Path(temp_directory) / "sample.md"
            markdown_file.write_text("테스트 문서", encoding="utf-8")

            with self.assertRaises(ValueError):
                read_text_document(markdown_file)

    def test_raises_when_file_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            empty_file = Path(temp_directory) / "empty.txt"
            empty_file.write_text("", encoding="utf-8")

            with self.assertRaises(ValueError):
                read_text_document(empty_file)
