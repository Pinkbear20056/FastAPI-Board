from pydantic import BaseModel, EmailStr
from datetime import datetime

# - UserCreate → 생성용
# - UserUpdate → 수정용
# - UserResponse → 응답용

# id = Column(Integer, primary_key = True, index = True)
# title = Column(String, nullable=False, index = True)
# content = Column(String, nullable=False)
# writer = Column(String, nullable=False)
# created_at = Column(DateTime, server_default=func.now())
# updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PostCreate(BaseModel):
  title: str
  content: str
  writer: str
  # created_at: datetime | None = None <- DB에 자동으로 시간이 생성돼서 ㄱㅊ음

class PostResponse(BaseModel):
  id: int # 구별하는 역할이고 보안이랑은 관련없음
  title: str
  content: str
  writer: str
  created_at: datetime | None = None
  updated_at: datetime | None = None

  model_config = {"from_attributes": True}

class PostUpdate(BaseModel):
  title: str | None = None
  content: str | None = None

