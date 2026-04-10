from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=300)
    filename: str = Field(min_length=1, max_length=255)
    pdfBase64: str | None = None


class ExtractResponse(BaseModel):
    extractedText: str
    status: str
    chunkCount: int


class GenerateQuestionsRequest(BaseModel):
    material_title: str = Field(min_length=1, max_length=100)
    material_text: str = Field(min_length=1, max_length=20000)
    question_count: int = Field(ge=1, le=10)


class GeneratedQuestion(BaseModel):
    stem: str
    options: list[str]
    correctOptionIndex: int
    explanation: str
    conceptTags: list[str]


class GenerateQuestionsResponse(BaseModel):
    questions: list[GeneratedQuestion]


class QaRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    context: str = Field(min_length=1, max_length=20000)


class QaResponse(BaseModel):
    answer: str
    evidenceSnippets: list[str]
    grounded: bool
    insufficientEvidence: bool
