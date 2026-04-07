# Extract Material API 상세

## 메서드 / URL
- `POST /extract-material`

## Request
| key | 타입 | 설명 | 필수 |
| --- | --- | --- | --- |
| title | string | 자료 제목 | Y |
| description | string | 자료 설명 | N |
| filename | string | 파일명 | Y |

## Response
| key | 타입 | 설명 |
| --- | --- | --- |
| extractedText | string | 추출 텍스트 |
| status | string | READY |
| chunkCount | number | LangChain splitter 결과 chunk 수 |
