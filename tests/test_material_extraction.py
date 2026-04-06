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
            "question_count": 3,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["questions"]) == 3
    assert all(len(question["options"]) == 4 for question in payload["questions"])
