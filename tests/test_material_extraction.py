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
