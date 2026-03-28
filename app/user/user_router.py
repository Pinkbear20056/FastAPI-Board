from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.user_model import User
from app.user.user_schema import UserUpdate, UserResponse
from app.user.user_repository import UserRepository
from app.user.user_service import UserService
from app.auth.auth_utils import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
        # Depends(get_current_user)가 API 실행 전에 아래 절차를 자동 수행:
        # 1) HTTPBearer가 요청 헤더에서 "Authorization: Bearer <토큰>" 추출
        #    → 헤더가 없으면 403 (Not authenticated)
        # 2) jwt.decode()로 토큰 검증
        #    → 시그니처 위조 여부 확인 (SECRET_KEY로 서명 검증)
        #    → 만료 시간(exp) 확인 → 만료되었으면 401
        # 3) payload에서 user_id(sub) 추출
        # 4) DB에서 user_id로 유저 조회 → 탈퇴한 유저면 401
        # → 모든 검증 통과 후 User 객체가 current_user에 전달됨
):
    """내 정보 조회 (토큰 필요)"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """내 정보 수정 (토큰 필요)"""
    # 인증된 current_user.id로만 수정 → 다른 유저의 정보를 변경할 수 없음
    return user_service.update_user(current_user.id, request)


@router.delete("/me", status_code=204)
def delete_me(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """회원 탈퇴 (토큰 필요)"""
    # 인증된 current_user.id로만 삭제 → 본인만 탈퇴 가능
    user_service.delete_user(current_user.id)
