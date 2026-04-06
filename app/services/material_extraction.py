from langchain_text_splitters import RecursiveCharacterTextSplitter


class MaterialExtractionService:
    def __init__(self) -> None:
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    def extract(self, title: str, description: str, filename: str) -> tuple[str, int]:
        """F2 자료 메타데이터를 기반으로 추출 텍스트와 chunk 수를 생성합니다."""
        extracted_text = (
            f"자료 제목: {title}\n"
            f"설명: {description}\n"
            f"파일명: {filename}\n"
            "이 텍스트는 LangChain 분할을 거친 MVP용 추출 결과입니다."
        )
        chunks = self._splitter.split_text(extracted_text)
        return extracted_text, len(chunks)
