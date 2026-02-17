from fastapi import File, UploadFile, APIRouter, Depends

from app.services.pdf_service import process_pdf
from app.schema.query_schema import QueryRequest, QueryResponse
from app.services.query_service import ask_llm, ask_llm_user
from app.core.security import get_current_user
import tempfile


router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: dict[str, str] = Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    process_pdf(tmp_path, file.filename, current_user.id)  # type: ignore

    return {"filename": file.filename, "status": "processed"}


@router.post("/query", response_model=QueryResponse)
async def query(
    request_data: QueryRequest, current_user: dict[str, str] = Depends(get_current_user)
):

    # response = ask_llm(question=request_data.question)
    response = ask_llm_user(question=request_data.question, user_id=current_user.id)  # type: ignore
    return {"question": request_data.question, "response": response}
