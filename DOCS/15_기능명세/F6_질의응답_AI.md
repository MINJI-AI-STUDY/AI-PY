# F6 질의응답 AI

## 범위
- `POST /qa`
- LangChain splitter 기반 근거 선택
- Gemini 응답 + fallback 응답

## 구현 원칙
- 질문 입력은 4000자 이하로 제한합니다.
- 근거 snippet은 최대 2개를 반환합니다.
- 모델 응답이 실패하거나 grounded false면 fallback 응답으로 닫습니다.
