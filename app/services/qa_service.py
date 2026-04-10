import re

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.schemas import QaResponse


class QaService:
    def __init__(self) -> None:
        self._llm = None
        self._embeddings = None
        if settings.google_api_key:
            google_api_key = settings.google_api_key.get_secret_value()
            self._llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=google_api_key,
                temperature=0.2,
            )
            self._embeddings = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=google_api_key,
                task_type="RETRIEVAL_DOCUMENT",
            )
        else:
            self._embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
        self._prompt = PromptTemplate.from_template(
            """
            너는 교육용 자료 기반 질의응답 도우미다.
            아래 검색된 근거 조각만 사용해서 답하라.
            답변은 반드시 아래 형식을 지켜라.

            [답변]
            - 질문에 대한 핵심 답을 1~3문장으로 쓴다.

            [근거 요약]
            - 근거 조각에서 확인되는 사실만 bullet 1~3개로 쓴다.

            [판단]
            - 충분한 근거가 있으면 '자료 근거로 답변함'
            - 부족하면 '자료에서 직접적인 근거를 찾기 어렵습니다.'

            절대 자료에 없는 내용을 추측해서 쓰지 마라.

            근거:
            {context}

            질문:
            {question}
            """.strip()
        )

    def ask(self, context: str, user_question: str) -> QaResponse:
        """F6 질의응답을 수행하고 실패 시 fallback 응답을 반환합니다."""
        snippets = self._retrieve_snippets(context, user_question)

        if self._llm is None:
            return self._fallback(user_question, snippets)

        try:
            prompt = self._prompt.format(context="\n\n".join(snippets), question=user_question)
            result = self._llm.invoke(prompt)
            answer = str(getattr(result, "content", result)).strip()
            insufficient = "자료에서 직접적인 근거를 찾기 어렵습니다." in answer
            if insufficient:
                return QaResponse(answer=answer, evidenceSnippets=[], grounded=False, insufficientEvidence=True)
            return QaResponse(answer=answer, evidenceSnippets=snippets[: settings.rag_top_k], grounded=True, insufficientEvidence=False)
        except Exception:
            return self._fallback(user_question, snippets)

    def _retrieve_snippets(self, context: str, user_question: str) -> list[str]:
        chunks = self._splitter.split_text(context)
        normalized_chunks = [self._normalize_chunk(chunk) for chunk in chunks if self._normalize_chunk(chunk)]
        if not normalized_chunks:
            return [context]
        if self._embeddings is None:
            return self._lexical_retrieve(normalized_chunks, user_question)

        try:
            documents = [Document(page_content=chunk, metadata={"chunk_index": index}) for index, chunk in enumerate(normalized_chunks)]
            vector_store = InMemoryVectorStore(self._embeddings)
            vector_store.add_documents(documents)
            retrieved = vector_store.similarity_search(user_question, k=min(settings.rag_top_k, len(documents)))
            snippets = [document.page_content for document in retrieved if document.page_content]
            return snippets or normalized_chunks[: settings.rag_top_k]
        except Exception:
            return self._lexical_retrieve(normalized_chunks, user_question)

    def _lexical_retrieve(self, chunks: list[str], user_question: str) -> list[str]:
        query_terms = set(re.findall(r"[가-힣A-Za-z0-9·]{2,}", user_question))
        ranked = sorted(
            chunks,
            key=lambda chunk: sum(1 for term in query_terms if term in chunk),
            reverse=True,
        )
        return ranked[: settings.rag_top_k]

    def _normalize_chunk(self, chunk: str) -> str:
        return re.sub(r"\s+", " ", chunk).strip()

    def _fallback(self, user_question: str, snippets: list[str]) -> QaResponse:
        supporting_sentences = self._select_supporting_sentences(snippets, user_question)
        summary_lines = [f"- {sentence}" for sentence in supporting_sentences[: settings.rag_top_k]]
        summary = "\n".join(summary_lines) if summary_lines else "- 자료에서 직접적인 근거를 찾기 어렵습니다."
        answer_line = supporting_sentences[0] if supporting_sentences else f"자료에서 직접적인 근거를 찾기 어렵습니다: {user_question}"
        grounded = bool(supporting_sentences)
        return QaResponse(
            answer=(
                "[답변]\n"
                f"- {answer_line}\n\n"
                "[근거 요약]\n"
                f"{summary}\n\n"
                "[판단]\n"
                f"- {'자료 근거로 답변함' if grounded else '자료에서 직접적인 근거를 찾기 어렵습니다.'}"
            ),
            evidenceSnippets=snippets[: settings.rag_top_k],
            grounded=grounded,
            insufficientEvidence=not grounded,
        )

    def _select_supporting_sentences(self, snippets: list[str], user_question: str) -> list[str]:
        query_terms = set(re.findall(r"[가-힣A-Za-z0-9·]{2,}", user_question))
        ranked_sentences: list[tuple[int, str]] = []
        for snippet in snippets:
            parts = re.split(r"[\n\.\?!]+", snippet)
            for part in parts:
                normalized = part.strip()
                if len(normalized) < 8:
                    continue
                score = sum(1 for term in query_terms if term in normalized)
                if "기준" in user_question and any(token in normalized for token in ["dB", "데시벨", "주간", "야간"]):
                    score += 3
                if any(char.isdigit() for char in normalized):
                    score += 1
                if score > 0 and all(existing != normalized for _, existing in ranked_sentences):
                    ranked_sentences.append((score, normalized))
        if ranked_sentences:
            ranked_sentences.sort(key=lambda item: item[0], reverse=True)
            return [sentence for _, sentence in ranked_sentences[: settings.rag_top_k]]
        return [snippet[:160].strip() for snippet in snippets if snippet.strip()][: settings.rag_top_k]
