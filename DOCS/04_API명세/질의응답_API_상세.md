# QA API 상세

## 메서드 / URL
- `POST /qa`

## Request
| key | 타입 | 설명 | 필수 |
| --- | --- | --- | --- |
| question | string | 사용자 질문(최대 500자) | Y |
| context | string | 추출된 문서 본문 | Y |

## Response
| key | 타입 | 설명 |
| --- | --- | --- |
| answer | string | 최종 응답 |
| evidenceSnippets | string[] | `rag_top_k` 범위 근거 snippet |
| grounded | boolean | grounded 여부 |
| insufficientEvidence | boolean | 근거 부족 여부 |

## 응답 형식 보장
- `answer`는 `[답변]`, `[근거 요약]`, `[판단]` 섹션을 포함하도록 정규화됩니다.
- 도메인 밖 질문은 차단 응답과 함께 `grounded=false`, `insufficientEvidence=true`를 반환합니다.
