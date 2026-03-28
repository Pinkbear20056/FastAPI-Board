from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.user_model import User
from app.user.user_repository import UserRepository

# ── 설정값 ──
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# HTTPBearer: 요청 헤더에서 "Authorization: Bearer ..." 토큰을 자동으로 추출
security = HTTPBearer()


# ── 비밀번호 해싱 ──

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해싱하여 반환"""
    # encode: 문자열 → 바이트 (bcrypt가 바이트를 요구)
    # gensalt: 매번 다른 랜덤 salt 생성 → 같은 비밀번호라도 다른 해시값
    # decode: 바이트 → 문자열 (DB에 문자열로 저장하기 위해)
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호가 해시값과 일치하는지 확인"""
    # checkpw가 내부적으로 해시값에서 salt를 추출하여 동일한 방식으로 해싱 후 비교
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ── JWT 토큰 ──

def create_access_token(user_id: int) -> str:
    """JWT 액세스 토큰 생성"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # sub(subject): 토큰의 주인 (JWT 표준 필드)
        "exp": expire,        # exp(expiration): 만료 시간 (JWT 표준 필드, 자동 검증됨)
    }
    # payload + SECRET_KEY → 서명된 토큰 문자열 생성
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
        # Depends(security)가 먼저 실행되어 헤더에서 "Bearer <토큰>" 자동 추출
        # → 헤더가 없으면 403 (Not authenticated)
    db: Session = Depends(get_db),
) -> User:
    """
    토큰 검증 + DB 유저 존재 확인까지 수행하는 인증 함수.
    라우터에서 Depends(get_current_user)로 사용하면
    검증된 User 객체를 바로 받을 수 있다.
    """
    # 1) 토큰 검증: 서명 위조 여부 + 만료 시간 확인 + payload 추출
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        # JWTError: 토큰 위조 또는 만료
        # ValueError/TypeError: sub 값이 없거나 int 변환 실패
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # 2) DB 조회: 탈퇴한 유저의 토큰인 경우 여기서 차단
    user = UserRepository(db).find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="존재하지 않는 유저입니다.")
    return user
