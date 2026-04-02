# DB table for post
# - 게시글 번호   -> id         Int 숫자 (1씩 자동으로 증가하는 숫자)
# - 게시글 제목    -> title         Str 문자 (숫자,영어, 특수문자 등)
# - 게시글 내용    -> content      Str 문자 (숫자,영어, 특수문자 등)
# - 작성자       -> writer       Int 숫자  
# - 시간         -> created_at    Date 타입 (날짜타입)
# - 수정시간    -> updated_at    Date 타입 (날짜타입)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
# DB 내부 함수 호출용

from app.database import Base


class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key = True, index = True)
  title = Column(String, nullable=False, index = True)
  content = Column(String, nullable=False)
  writer = Column(String, nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

