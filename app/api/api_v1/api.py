from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, pdfs

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(pdfs.router, prefix="/pdfs", tags=["PDFs"])
