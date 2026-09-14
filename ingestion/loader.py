from pathlib import Path

import pymupdf


class DocumentLoader:
    """Load supported document formats into plain text."""

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}

    def load(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")

        return self._load_pdf(path)

    def _load_pdf(self, path: Path) -> str:
        pages = []

        with pymupdf.open(path) as document:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(text)

        return "\n\n".join(pages)


loader = DocumentLoader()