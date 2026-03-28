import logging

from fastapi import HTTPException

from app.user.user_model import User
from app.user.user_schema import UserUpdate
from app.user.user_repository import UserRepository

logger = logging.getLogger("uvicorn")


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:
        logger.info(f"유저 조회: id={user_id}")
        user = self.user_repository.find_by_id(user_id)
        if not user:
            logger.info(f"유저 조회 실패: id={user_id} 없음")
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        return user

    def update_user(self, user_id: int, request: UserUpdate) -> User:
        logger.info(f"유저 수정 요청: id={user_id}, fields={request.model_dump(exclude_none=True)}")
        user = self.get_user(user_id)

        if request.name is not None:
            user.name = request.name
        if request.email is not None:
            # 이메일 중복 체크: 다른 유저가 이미 사용 중인지 확인
            # existing.id != user_id: 본인이 현재 쓰고 있는 이메일은 중복이 아님
            existing = self.user_repository.find_by_email(request.email)
            if existing and existing.id != user_id:
                logger.info(f"유저 수정 실패: 이메일 중복 ({request.email})")
                raise HTTPException(status_code=409, detail="이미 존재하는 이메일입니다.")
            user.email = request.email

        saved = self.user_repository.save(user)
        logger.info(f"유저 수정 완료: id={saved.id}")
        return saved

    def delete_user(self, user_id: int) -> None:
        logger.info(f"유저 삭제 요청: id={user_id}")
        user = self.get_user(user_id)
        self.user_repository.delete(user)
        logger.info(f"유저 삭제 완료: id={user_id}")
