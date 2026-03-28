import logging

from fastapi import HTTPException

from app.user.user_model import User
from app.user.user_repository import UserRepository
from app.auth.auth_utils import hash_password, verify_password, create_access_token
from app.auth.auth_schema import SignupRequest, LoginRequest, TokenResponse

logger = logging.getLogger("uvicorn")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup(self, request: SignupRequest) -> User:
        """회원가입: 이메일 중복 체크 + 비밀번호 해싱 후 저장"""
        logger.info(f"회원가입 요청: email={request.email}")

        if self.user_repository.find_by_email(request.email):
            logger.info(f"회원가입 실패: 이메일 중복 ({request.email})")
            raise HTTPException(status_code=409, detail="이미 존재하는 이메일입니다.")

        hashed = hash_password(request.password)
        user = User(
            name=request.name,
            email=request.email,
            password=hashed
        )
        saved = self.user_repository.save(user)
        logger.info(f"회원가입 완료: id={saved.id}")
        return saved

    def login(self, request: LoginRequest) -> TokenResponse:
        """로그인: 이메일/비밀번호 검증 후 JWT 토큰 발급"""
        logger.info(f"로그인 요청: email={request.email}")

        find_user = self.user_repository.find_by_email(request.email)
        if not find_user:
            logger.info(f"로그인 실패: 이메일 없음 ({request.email})")
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")

        if not verify_password(request.password, find_user.password):
            logger.info(f"로그인 실패: 비밀번호 불일치 ({request.email})")
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")
        # 보안: 이메일 없음 / 비밀번호 틀림 모두 동일한 에러 메시지를 반환
        # → 해커가 "이 이메일이 가입되어 있는지" 유추할 수 없도록 방지

        token = create_access_token(find_user.id)
        logger.info(f"로그인 성공: id={find_user.id}")
        return TokenResponse(access_token=token)
