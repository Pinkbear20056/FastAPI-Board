# 일단 import도 멀해야할 지 모르겠어서 아래부터 작성해보자!
# 필요할 때마다 하나씩 추가해보기!
from fastapi import APIRouter, Depends, HTTPException

from app.post.post_schema import PostResponse, PostCreate, PostUpdate
from app.database import get_db
from app.post.post_model import Post

from sqlalchemy.orm import Session

# 구현할 기능들 4가지
# Create: 게시글 작성, Read: 게시글 조회, Upadate: 게시글 수정, Delete: 게시글 삭제

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

# Create: 게시글 작성 - 생성 - POST
@router.post("", response_model=PostResponse, status_code=201)
def create_post(user_in: PostCreate, db: Session = Depends(get_db)): # 여기까지로 from import 필요한거 작성 가능
  post = Post(
    title = user_in.title,
    content = user_in.content,
    writer = user_in.writer,
  )
  db.add(post)
  db.commit()
  db.refresh(post)
  return post

# Read: 게시글 조회 - GET
# 전체 유저 조회
@router.get("", response_model=list[PostResponse])
def get_post(db: Session = Depends(get_db)): #이 db 객체는 되돌려줄때 만듦??
  return db.query(Post).all()
  
# 단건 조회

# Upadate: 게시글 수정 - PUT
# Delete: 게시글 삭제 - DELETE