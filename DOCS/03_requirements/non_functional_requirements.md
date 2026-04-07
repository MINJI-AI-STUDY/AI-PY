# 비기능 요구사항 명세서

| ID | 업무구분 | 요구사항 명 | 상세 설명 |
| --- | --- | --- | --- |
| NFR-AI-001 | 안정성 | fallback 보장 | LLM 호출 실패 시 deterministic fallback으로 응답을 닫는다. |
| NFR-AI-002 | 보안 | API 키 비노출 | `GOOGLE_API_KEY`는 `.env`로만 주입하고 저장소에 커밋하지 않는다. |
| NFR-AI-003 | 일관성 | 구조화 응답 | 생성/QA 응답은 고정된 JSON 구조를 유지한다. |
