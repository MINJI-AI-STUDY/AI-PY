from fastapi import FastAPI

from app.schemas import ExtractRequest, ExtractResponse
from app.services.material_extraction import MaterialExtractionService


app = FastAPI(title="AI-STUDY AI-PY", version="0.1.0")
material_extraction_service = MaterialExtractionService()


@app.get("/health")
def health() -> dict[str, str]:
    """AI 서비스 상태를 반환합니다."""
    return {"status": "ok", "service": "ai-py", "port": "8000"}


@app.post("/extract-material", response_model=ExtractResponse)
def extract_material(request: ExtractRequest) -> ExtractResponse:
    """F2 자료 추출 결과와 chunk 수를 반환합니다."""
    extracted_text, chunk_count = material_extraction_service.extract(
        title=request.title,
        description=request.description,
        filename=request.filename,
    )
    return ExtractResponse(extractedText=extracted_text, status="READY", chunkCount=chunk_count)
