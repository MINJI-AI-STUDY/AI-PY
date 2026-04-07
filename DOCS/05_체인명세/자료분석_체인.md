# Material Extraction Chain

## 입력
- `title`
- `description`
- `filename`

## 단계
1. metadata 문자열 구성
2. `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)` 적용
3. 추출 텍스트와 chunkCount 반환

## 출력
- `extractedText`
- `chunkCount`
- `status=READY`
