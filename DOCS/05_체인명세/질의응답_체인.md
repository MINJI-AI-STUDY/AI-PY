# QA Chain

## 입력
- raw `question` 문자열 (context + question)

## 단계
1. `질문:` delimiter로 context/question 분리
2. `RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)`로 snippet 후보 생성
3. 최대 2개 snippet 선택
4. Gemini 응답 호출
5. grounded false 또는 예외 시 fallback 응답 반환

## 출력
- `answer`
- `evidenceSnippets[0..2]`
- `grounded`
- `insufficientEvidence`
