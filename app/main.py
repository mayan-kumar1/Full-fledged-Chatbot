from fastapi import FastAPI
from app.api.api_v1.api import api_router
from contextlib import asynccontextmanager
from app.services import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.users import User

    database.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(title="Chat with PDFs", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
