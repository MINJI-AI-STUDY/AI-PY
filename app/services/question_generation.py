import json
import re
from typing import Any

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.schemas import GeneratedQuestion


class QuestionGenerationService:
    def __init__(self) -> None:
        self._llm = None
        if settings.google_api_key:
            self._llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.google_api_key,
                temperature=0.3,
            )
        self._prompt = PromptTemplate.from_template(
            """
            너는 교육용 객관식 문항 생성기다.
            아래 자료 본문을 바탕으로 {question_count}개의 4지선다 객관식 문항을 JSON 배열로 생성해라.
            각 문항은 stem, options(4개), correctOptionIndex(0~3), explanation, conceptTags(1~2개)만 포함한다.
            다른 설명 없이 JSON만 반환해라.

            자료 제목: {material_title}
            자료 본문:
            {material_text}
            """.strip()
        )

    def generate(self, material_title: str, material_text: str, question_count: int) -> list[GeneratedQuestion]:
        """F3 문항 생성을 수행하고, 실패 시 deterministic fallback을 반환합니다."""
        if self._llm is None:
            return self._fallback(material_title, material_text, question_count)

        try:
            prompt = self._prompt.format(material_title=material_title, material_text=material_text[:6000], question_count=question_count)
            result = self._llm.invoke(prompt)
            content = getattr(result, "content", result)
            payload = self._parse_json(content)
            questions = [GeneratedQuestion(**item) for item in payload]
            if len(questions) != question_count:
                return self._fallback(material_title, material_text, question_count)
            return questions
        except Exception:
            return self._fallback(material_title, material_text, question_count)

    def _parse_json(self, content: Any) -> list[dict[str, Any]]:
        text = str(content).strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text)

    def _fallback(self, material_title: str, material_text: str, question_count: int) -> list[GeneratedQuestion]:
        keywords = self._extract_keywords(material_text, question_count)
        return [
            GeneratedQuestion(
                stem=f"{material_title} 자료에서 '{keywords[index - 1] if len(keywords) >= index else material_title}'와 가장 관련된 내용을 고르세요.",
                options=[keywords[index - 1] if len(keywords) >= index else f"핵심어 {index}", "오답 후보 A", "오답 후보 B", "오답 후보 C"],
                correctOptionIndex=0,
                explanation=f"{material_title} 본문에서 추출한 핵심어를 기준으로 생성한 해설입니다.",
                conceptTags=[keywords[index - 1] if len(keywords) >= index else f"핵심개념{index}"],
            )
            for index in range(1, question_count + 1)
        ]

    def _extract_keywords(self, material_text: str, question_count: int) -> list[str]:
        matches = re.findall(r"[가-힣A-Za-z0-9·]{2,}", material_text)
        deduped: list[str] = []
        for word in matches:
            if word not in deduped:
                deduped.append(word)
        return deduped[: max(question_count, 3)]
