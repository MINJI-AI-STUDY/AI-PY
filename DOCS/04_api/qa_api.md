# QA API 상세

## 메서드 / URL
- `POST /qa`

## Request
| key | 타입 | 설명 | 필수 |
| --- | --- | --- | --- |
| question | string | context + 질문 문자열 | Y |

## Response
| key | 타입 | 설명 |
| --- | --- | --- |
| answer | string | 최종 응답 |
| evidenceSnippets | string[] | 최대 2개 근거 snippet |
| grounded | boolean | grounded 여부 |
| insufficientEvidence | boolean | 근거 부족 여부 |
