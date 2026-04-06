# F3 문항 생성 AI

## 범위
- `POST /generate-questions`
- LangChain PromptTemplate + Gemini 기반 객관식 문항 생성

## 구현 원칙
- 문항 수는 1~10개만 허용합니다.
- 각 문항은 4지선다, 정답 1개, explanation, conceptTags 1~2개를 가집니다.
- LLM 응답 파싱 실패 시 deterministic fallback으로 문항을 반환합니다.
