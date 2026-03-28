from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
