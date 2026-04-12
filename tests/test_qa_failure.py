"""QA failure handling tests for AI-PY.

Tests that the /qa endpoint properly distinguishes between:
- Upstream connectivity failures (insufficientEvidence=False)
- Insufficient evidence responses (insufficientEvidence=True)
- Out-of-domain questions (insufficientEvidence=True)
- Empty question validation (insufficientEvidence=True)
"""
import pytest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from app.main import app
from app.schemas import QaResponse

client = TestClient(app)


class TestQaConnectivityFailure:
    """Tests for AI service connectivity failure handling."""

    def test_qa_endpoint_returns_200_on_internal_exception(self, monkeypatch):
        """When qa_service.ask() raises an exception, the endpoint should return 200
        with insufficientEvidence=False (service error, not evidence shortage)."""
        from app.main import qa_service

        def _raise(context, question):
            raise RuntimeError("LLM connection refused")

        monkeypatch.setattr(qa_service, "ask", _raise)

        response = client.post(
            "/qa",
            json={"question": "핵심 개념이 뭐야?", "context": "자료 핵심 개념 설명"},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["grounded"] is False
        assert payload["insufficientEvidence"] is False
        assert "오류가 발생했습니다" in payload["answer"]

    def test_qa_endpoint_empty_question_returns_insufficient_evidence(self):
        """Empty question should return insufficientEvidence=True (user error, not service error)."""
        response = client.post(
            "/qa",
            json={"question": "", "context": "자료 핵심 개념 설명"},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["grounded"] is False
        assert payload["insufficientEvidence"] is True
        assert "질문을 입력해주세요" in payload["answer"]


class TestQaInsufficientEvidence:
    """Tests for insufficient evidence vs connectivity failure distinction."""

    def test_qa_out_of_domain_returns_insufficient_evidence(self):
        """Out-of-domain questions should return insufficientEvidence=True."""
        response = client.post(
            "/qa",
            json={
                "question": "은행 대출 금리랑 주택담보대출 조건 알려줘",
                "context": "이 문서는 지수와 로그, 데시벨, 층간 소음 기준을 설명한다.",
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["grounded"] is False
        assert payload["insufficientEvidence"] is True

    def test_qa_fallback_response_preserves_insufficient_evidence_flag(self, monkeypatch):
        """When LLM is unavailable, fallback should return insufficientEvidence based on evidence availability."""
        from app.main import qa_service

        monkeypatch.setattr(qa_service, "_llm", None)
        monkeypatch.setattr(
            qa_service,
            "_retrieve_snippets",
            lambda context, question: ["자료 핵심 개념 설명"],
        )

        response = client.post(
            "/qa",
            json={"question": "핵심 개념이 뭐야?", "context": "자료 핵심 개념 설명"},
        )
        assert response.status_code == 200
        payload = response.json()
        # Fallback with supporting sentences should have grounded=True
        assert payload["grounded"] is True
        assert payload["insufficientEvidence"] is False


class TestQaResponseSchema:
    """Tests that verify the response schema contract is preserved."""

    def test_qa_response_has_required_fields(self, monkeypatch):
        """All QA responses must have answer, evidenceSnippets, grounded, insufficientEvidence."""
        from app.main import qa_service

        monkeypatch.setattr(
            qa_service,
            "ask",
            lambda context, question: QaResponse(
                answer="테스트 답변",
                evidenceSnippets=["근거1"],
                grounded=True,
                insufficientEvidence=False,
            ),
        )

        response = client.post(
            "/qa",
            json={"question": "테스트 질문", "context": "테스트 컨텍스트"},
        )
        assert response.status_code == 200
        payload = response.json()
        assert "answer" in payload
        assert "evidenceSnippets" in payload
        assert "grounded" in payload
        assert "insufficientEvidence" in payload

    def test_qa_service_error_distinguished_from_evidence_shortage(self, monkeypatch):
        """Service errors (insufficientEvidence=False) should be distinguishable from
        evidence shortage (insufficientEvidence=True) in the response schema."""
        from app.main import qa_service

        # Simulate connectivity failure
        def _connectivity_failure(context, question):
            raise ConnectionError("AI server unreachable")

        monkeypatch.setattr(qa_service, "ask", _connectivity_failure)

        response = client.post(
            "/qa",
            json={"question": "질문", "context": "컨텍스트"},
        )
        payload = response.json()
        connectivity_failure_insufficient = payload["insufficientEvidence"]

        # Simulate insufficient evidence
        monkeypatch.setattr(
            qa_service,
            "ask",
            lambda context, question: QaResponse(
                answer="근거 부족",
                evidenceSnippets=[],
                grounded=False,
                insufficientEvidence=True,
            ),
        )

        response = client.post(
            "/qa",
            json={"question": "질문", "context": "컨텍스트"},
        )
        payload = response.json()
        evidence_shortage_insufficient = payload["insufficientEvidence"]

        # The two should be distinguishable
        assert connectivity_failure_insufficient is False
        assert evidence_shortage_insufficient is True