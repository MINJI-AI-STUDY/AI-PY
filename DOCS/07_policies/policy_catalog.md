# AI 정책 카탈로그

| 정책 코드 | 정책명 | 항목 | 설명 | 정책 정의 | 관련 기능군 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| AI-P-00-001 | 분석 정책 | chunk 계산 | 자료 분석 | 추출 결과는 chunk 수를 함께 반환한다. | F2 | splitter 기반 |
| AI-P-00-002 | 생성 정책 | 4지선다 구조 | 문항 생성 | 4지선다, 정답 1개, explanation, conceptTags 1~2개를 유지한다. | F3 | fallback 동일 구조 |
| AI-P-00-003 | QA 정책 | grounded QA | 질의응답 | 근거 snippet은 최대 2개, grounded false면 fallback 가능 | F6 | |
| AI-P-00-004 | 생성 정책 | 생성 수 정합성 | 문항 생성 | 생성 결과 수가 요청 수와 다르면 fallback으로 닫는다. | F3 | 품질 하한 |
| AI-P-00-005 | QA 정책 | 질문 길이 | 질의응답 | QA 입력은 최대 4000자까지 허용한다. | F6 | raw context 포함 |
| AI-P-00-006 | QA 정책 | fallback | 질의응답 | 모델 실패 또는 grounded false면 deterministic fallback 응답을 사용한다. | F6 | 운영 안정성 |
