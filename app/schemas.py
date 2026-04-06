from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=300)
    filename: str = Field(min_length=1, max_length=255)


class ExtractResponse(BaseModel):
    extractedText: str
    status: str
    chunkCount: int
