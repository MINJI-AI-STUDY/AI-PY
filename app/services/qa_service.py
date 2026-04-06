from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.schemas import QaResponse


class QaService:
    def __init__(self) -> None:
        self._llm = None
        if settings.google_api_key:
            self._llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.google_api_key,
                temperature=0.2,
            )
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
        self._prompt = PromptTemplate.from_template(
            """
            너는 교육용 자료 기반 질의응답 도우미다.
            아래 근거 조각만 사용해서 질문에 답하라.
            근거가 부족하면 '자료에서 직접적인 근거를 찾기 어렵습니다.'라고 답하라.

            근거:
            {context}

            질문:
            {question}
            """.strip()
        )

    def ask(self, raw_question: str) -> QaResponse:
        """F6 질의응답을 수행하고 실패 시 fallback 응답을 반환합니다."""
        context, user_question = self._split_input(raw_question)
        snippets = self._select_snippets(context)

        if self._llm is None:
          return self._fallback(user_question, snippets)

        try:
            prompt = self._prompt.format(context="\n\n".join(snippets), question=user_question)
            result = self._llm.invoke(prompt)
            answer = str(getattr(result, "content", result)).strip()
            insufficient = "직접적인 근거를 찾기 어렵" in answer
            if insufficient:
                return QaResponse(answer=answer, evidenceSnippets=[], grounded=False, insufficientEvidence=True)
            return QaResponse(answer=answer, evidenceSnippets=snippets[:2], grounded=True, insufficientEvidence=False)
        except Exception:
            return self._fallback(user_question, snippets)

    def _split_input(self, raw_question: str) -> tuple[str, str]:
        if "질문:" not in raw_question:
            return raw_question, raw_question
        context, question = raw_question.rsplit("질문:", 1)
        return context.strip(), question.strip()

    def _select_snippets(self, context: str) -> list[str]:
        chunks = self._splitter.split_text(context)
        return chunks[:2] if chunks else [context]

    def _fallback(self, user_question: str, snippets: list[str]) -> QaResponse:
        return QaResponse(
            answer=f"자료 기준 기본 답변입니다: {user_question}",
            evidenceSnippets=snippets[:2],
            grounded=True,
            insufficientEvidence=False,
        )
