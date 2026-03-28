from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.user_repository import UserRepository
from app.auth.auth_schema import SignupRequest, SignupResponse, LoginRequest, TokenResponse
from app.auth.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(request: SignupRequest, auth_service: AuthService = Depends(get_auth_service)):
    """회원가입"""
    return auth_service.signup(request)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """로그인 → 토큰 발급"""
    return auth_service.login(request)
