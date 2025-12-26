"""
pdf_parser.py

Phase 1: PDF Parsing & Text Preprocessing
"""

import re
from PyPDF2 import PdfReader


def extract_pdf_text(pdf_path: str) -> str:
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()


def extract_and_clean(pdf_path: str) -> str:
    return clean_text(extract_pdf_text(pdf_path))
