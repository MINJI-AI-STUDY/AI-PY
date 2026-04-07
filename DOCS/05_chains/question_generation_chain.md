# Question Generation Chain

## 입력
- `material_title`
- `question_count`

## 단계
1. PromptTemplate 생성
2. `ChatGoogleGenerativeAI(model="gemini-2.5-flash")` 호출
3. JSON 문자열 파싱
4. `GeneratedQuestion` 스키마 검증
5. 생성 수 불일치/파싱 실패 시 fallback 전환

## 출력
- 4지선다 문항 배열

## 실패 전략
- deterministic fallback 생성
