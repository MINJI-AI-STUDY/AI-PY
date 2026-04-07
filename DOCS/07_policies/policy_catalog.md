# AI 정책 카탈로그

| 정책 코드 | 정책명 | 항목 | 설명 | 정책 정의 | 관련 기능군 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| AI-P-00-001 | 분석 정책 | chunk 계산 | 자료 분석 | 추출 결과는 chunk 수를 함께 반환한다. | F2 | splitter 기반 |
| AI-P-00-002 | 생성 정책 | 4지선다 구조 | 문항 생성 | 4지선다, 정답 1개, explanation, conceptTags 1~2개를 유지한다. | F3 | fallback 동일 구조 |
| AI-P-00-003 | QA 정책 | grounded QA | 질의응답 | 근거 snippet은 최대 2개, grounded false면 fallback 가능 | F6 | |
