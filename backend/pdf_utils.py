"""PDF text extraction utilities."""

from PyPDF2 import PdfReader
from io import BytesIO
from typing import List, Dict


def extract_text_from_pdf(file_bytes: bytes, doc_name: str) -> List[Dict]:
    """
    Extract text from a PDF file, page by page.
    
    Returns a list of dicts:
      { "doc_name": str, "page_number": int, "text": str }
    """
    reader = PdfReader(BytesIO(file_bytes))
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append({
                "doc_name": doc_name,
                "page_number": i + 1,
                "text": text,
            })

    return pages
