from fastapi import FastAPI

from app.config import settings
from app.schemas import ExtractRequest, ExtractResponse, GenerateQuestionsRequest, GenerateQuestionsResponse, QaResponse
from app.services.material_extraction import MaterialExtractionService
from app.services.question_generation import QuestionGenerationService
from app.services.qa_service import QaService


app = FastAPI(title="AI-STUDY AI-PY", version="0.1.0")
material_extraction_service = MaterialExtractionService()
question_generation_service = QuestionGenerationService()
qa_service = QaService()


@app.get("/health")
def health() -> dict[str, str]:
    """AI 서비스 상태를 반환합니다."""
    return {"status": "ok", "service": "ai-py", "port": str(settings.ai_port)}


@app.post("/extract-material", response_model=ExtractResponse)
def extract_material(request: ExtractRequest) -> ExtractResponse:
    """F2 자료 추출 결과와 chunk 수를 반환합니다."""
    extracted_text, chunk_count = material_extraction_service.extract(
        title=request.title,
        description=request.description,
        filename=request.filename,
        pdf_base64=request.pdfBase64,
    )
    return ExtractResponse(extractedText=extracted_text, status="READY", chunkCount=chunk_count)


@app.post("/generate-questions", response_model=GenerateQuestionsResponse)
def generate_questions(request: GenerateQuestionsRequest) -> GenerateQuestionsResponse:
    """F3 객관식 문항 생성을 수행합니다."""
    questions = question_generation_service.generate(
        material_title=request.material_title,
        material_text=request.material_text,
        question_count=request.question_count,
    )
    return GenerateQuestionsResponse(questions=questions)


@app.post("/qa", response_model=QaResponse)
def qa(request: dict) -> QaResponse:
    """F6 자료 기반 질문 응답을 반환합니다."""
    question = str(request.get("question", "")).strip()
    raw_context = request.get("context", "")
    if isinstance(raw_context, list):
        context = " ".join(str(item) for item in raw_context)
    else:
        context = str(raw_context)
    return qa_service.ask(context, question)
