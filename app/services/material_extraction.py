import base64
import io
import re

import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


class MaterialExtractionService:
    def __init__(self) -> None:
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    def extract(self, title: str, description: str, filename: str, pdf_base64: str | None) -> tuple[str, int]:
        """F2 실제 PDF 텍스트를 우선 추출하고, 실패 시 메타데이터 fallback을 사용합니다."""
        extracted_text = self._extract_pdf_text(pdf_base64)
        if not extracted_text:
            extracted_text = self._fallback_text(title, description, filename)
        chunks = self._splitter.split_text(extracted_text)
        return extracted_text, len(chunks)

    def _extract_pdf_text(self, pdf_base64: str | None) -> str:
        if not pdf_base64:
            return ""
        try:
            pdf_bytes = base64.b64decode(pdf_base64)
            text = self._extract_with_pymupdf(pdf_bytes)
            if text:
                return text
        except Exception:
            return ""

        try:
            pdf_bytes = base64.b64decode(pdf_base64)
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pages = [page.extract_text() or "" for page in reader.pages]
            return self._normalize_text("\n".join(page.strip() for page in pages if page.strip()))
        except Exception:
            return ""

    def _extract_with_pymupdf(self, pdf_bytes: bytes) -> str:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            pages = [str(page.get_text("text")) for page in document]
        return self._normalize_text("\n".join(page for page in pages if page))

    def _normalize_text(self, text: str) -> str:
        cleaned = text.replace("\x00", " ")
        cleaned = re.sub(r"\(cid:\d+\)", " ", cleaned)
        cleaned = re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f]", " ", cleaned)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    def _fallback_text(self, title: str, description: str, filename: str) -> str:
        return (
            f"자료 제목: {title}\n"
            f"설명: {description}\n"
            f"파일명: {filename}\n"
            "PDF 본문 추출에 실패하여 메타데이터 기반 fallback 텍스트를 사용합니다."
        )
