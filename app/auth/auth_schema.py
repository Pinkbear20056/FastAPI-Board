from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupRequest(BaseModel):
    """회원가입 요청"""
    name: str
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    """회원가입 응답 (비밀번호는 절대 응답에 포함하지 않음!)"""
    id: int
    name: str
    email: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """토큰 응답"""
    access_token: str
    token_type: str = "bearer"
