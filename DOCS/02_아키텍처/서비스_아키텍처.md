# AI 서비스 아키텍처

## 원칙
- FastAPI는 HTTP contract를 담당
- LangChain service는 chain orchestration을 담당
- Gemini는 generation/qa의 LLM backend로 사용
- fallback 경로는 deterministic 응답으로 유지
