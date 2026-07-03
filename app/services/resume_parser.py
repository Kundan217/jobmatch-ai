import re
from pathlib import Path

import fitz


def extract_pdf_text(path: Path) -> str:
    text_parts: list[str] = []
    with fitz.open(path) as document:
        for page in document:
            text_parts.append(page.get_text("text"))
    return clean_text("\n".join(text_parts))


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()
