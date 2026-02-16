from pydantic import BaseModel, EmailStr
from typing import Optional


# This defines what the API expects when someone registers
class UserCreate(BaseModel):
    username: str
    email: EmailStr  # This validates that it's a real email format
    password: str


# This defines what the API sends back to the frontend
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        # This tells Pydantic to play nice with SQLAlchemy models
        from_attributes = True
