from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["port"] == "8000"


def test_extract_material_returns_ready_with_chunk_count() -> None:
    response = client.post(
        "/extract-material",
        json={
            "title": "수업 자료",
            "description": "분석용 설명",
            "filename": "sample.pdf",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "READY"
    assert payload["chunkCount"] >= 1
    assert "수업 자료" in payload["extractedText"]


def test_generate_questions_returns_requested_count() -> None:
    response = client.post(
        "/generate-questions",
        json={
            "material_title": "수업 자료",
            "material_text": "수업 자료의 핵심 개념은 분수의 덧셈과 통분이다.",
            "question_count": 3,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["questions"]) == 3
    assert all(len(question["options"]) == 4 for question in payload["questions"])


def test_qa_returns_fallback_shape(monkeypatch) -> None:
    from app.main import qa_service

    monkeypatch.setattr(
        qa_service,
        "ask",
        lambda context, question: {
            "answer": "자료 기준 기본 답변입니다: 핵심 개념이 뭐야?",
            "evidenceSnippets": ["자료 핵심 개념 설명"],
            "grounded": True,
            "insufficientEvidence": False,
        },
    )

    response = client.post("/qa", json={"question": "핵심 개념이 뭐야?", "context": "자료 핵심 개념 설명"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["grounded"] is True
    assert payload["answer"]


def test_qa_normalizes_non_sectioned_answer(monkeypatch) -> None:
    from app.main import qa_service

    class DummyResult:
        content = "층간 소음 기준은 주간 40 dB, 야간 50 dB입니다."

    class DummyLlm:
        def invoke(self, prompt: str) -> DummyResult:
            return DummyResult()

    monkeypatch.setattr(qa_service, "_llm", DummyLlm())
    monkeypatch.setattr(
        qa_service,
        "_retrieve_snippets",
        lambda context, question: [
            "층간 소음 기준은 주간 40 dB, 야간 50 dB이다.",
            "어른의 발뒤꿈치 소리가 40 dB, 의자 끄는 소리가 60 dB 정도이다.",
        ],
    )

    response = client.post("/qa", json={"question": "층간 소음 기준은 어느 정도야?", "context": "dummy context"})
    assert response.status_code == 200
    payload = response.json()
    assert "[답변]" in payload["answer"]
    assert "[근거 요약]" in payload["answer"]
    assert "[판단]" in payload["answer"]


def test_qa_blocks_out_of_domain_question() -> None:
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
    assert "현재 업로드된 문서와 학습 도메인 안에서만 답변할 수 있습니다." in payload["answer"]
