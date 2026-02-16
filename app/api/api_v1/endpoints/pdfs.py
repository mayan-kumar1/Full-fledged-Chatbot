from fastapi import File, UploadFile, APIRouter, Depends

from app.services.pdf_service import process_pdf
from app.schema.query_schema import QueryRequest, QueryResponse
from app.services.query_service import ask_llm
from app.core.security import get_current_user
import tempfile

is_pdf_uploaded: bool = False

router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    process_pdf(tmp_path, file.filename)

    global is_pdf_uploaded
    is_pdf_uploaded = True

    return {"filename": file.filename, "status": "processed"}


@router.post("/query", response_model=QueryResponse)
async def query(
    request_data: QueryRequest, current_user: dict[str, str] = Depends(get_current_user)
):

    if not is_pdf_uploaded:
        return {
            "question": request_data.question,
            "response": "Plasse upload pdf first",
        }

    response = ask_llm(question=request_data.question)
    return {"question": request_data.question, "response": response}
