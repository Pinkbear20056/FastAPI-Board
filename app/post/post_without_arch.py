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
def get_posts(db: Session = Depends(get_db)): #이 db 객체는 되돌려줄때 만듦??
  return db.query(Post).all()
  
# 단건 조회
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  return post
# user_in 은 작성자 혹은 게시글임
  

# Upadate: 게시글 수정 - PUT, 제목과 내용만 가능
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, user_in: PostUpdate, db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  
  if user_in.title is not None: 
    post.title = user_in.title
  if user_in.content is not None:
    post.content = user_in.content

  db.commit()
  db.refresh(post)
  return post

# Delete: 게시글 삭제 - DELETE
# response_model 없음
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)): #받는 정보는 id임
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post: 
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  
  db.delete(post)
  db.commit
