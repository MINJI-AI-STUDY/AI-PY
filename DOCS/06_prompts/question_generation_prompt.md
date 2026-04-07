# Question Generation Prompt

```text
너는 교육용 객관식 문항 생성기다.
아래 자료 제목을 바탕으로 {question_count}개의 4지선다 객관식 문항을 JSON 배열로 생성해라.
각 문항은 stem, options(4개), correctOptionIndex(0~3), explanation, conceptTags(1~2개)만 포함한다.
다른 설명 없이 JSON만 반환해라.

자료 제목: {material_title}
```

## 변수
- `material_title`
- `question_count`
