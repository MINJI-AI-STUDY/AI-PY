# QA Chain

## 현재 구조
- raw question에서 context/question 분리
- RecursiveCharacterTextSplitter로 snippet 2개 선택
- Gemini 답변
- 실패/grounded false 시 fallback
