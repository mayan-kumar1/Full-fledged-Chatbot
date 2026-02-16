from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.auth.auth_service import validate_user
from app.schema.users import UserCreate
from app.services.database import get_db
from app.services.users_service import create_user
from app.core.security import create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db),
):
    logger.info(f"Login attempt for user: {form_data.username}")
    print(f"Login attempt for user: {form_data.username}")
    user = validate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=201)
async def signup(user: UserCreate, db=Depends(get_db)):
    db_user = create_user(db, user)
    return {"username": db_user.username, "email": db_user.email}
