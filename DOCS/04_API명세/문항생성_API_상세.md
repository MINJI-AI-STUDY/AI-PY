# Generate Questions API 상세

## 메서드 / URL
- `POST /generate-questions`

## Request
| key | 타입 | 설명 | 필수 |
| --- | --- | --- | --- |
| material_title | string | 자료 제목 | Y |
| material_text | string | 자료 본문 텍스트 | Y |
| question_count | number | 문항 수(1~10) | Y |

## Response
- `questions[]`
  - `stem`
  - `options[4]`
  - `correctOptionIndex`
  - `explanation`
  - `conceptTags[1..2]`

## fallback
- Gemini 실패 시 deterministic fallback 문항 반환

## 구현 참고
- 실제 프롬프트에는 `material_text[:6000]`이 사용됩니다.
