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
# 응답 처리 - post_router.py
@router.post("", response_model=PostResponse, status_code=201)
# 요청 처리 - post_router.py
def create_post(user_in: PostCreate, db: Session = Depends(get_db)): # 여기까지로 from import 필요한거 작성 가능
  # 요청으로 받은 데이터를 ORM 모델 객체(Post)로 만드는 것
  # 비즈니스 로직은 아닌데 위치상 service에 넣기
  post = Post(
    title = user_in.title,
    content = user_in.content,
    writer = user_in.writer,
  )
  # DB 접근 - post_repository.py
  db.add(post)
  db.commit()
  db.refresh(post)
  # 응답 처리 - post_router.py
  return post

# Read: 게시글 조회 - GET
# 전체 유저 조회
# 응답 처리 - post_router.py
@router.get("", response_model=list[PostResponse])
# 요청 처리 - post_router.py
def get_posts(db: Session = Depends(get_db)): #이 db 객체는 되돌려줄때 만듦??
  # 응답 처리 - post_router.py
  return db.query(Post).all()
  
# 단건 조회
# 응답 처리 - post_router.py
@router.get("/{post_id}", response_model=PostResponse)
# 요청 처리 - post_router.py
def get_post(post_id: int, db: Session = Depends(get_db)):
  # 비즈니스 로직 - post_service.py
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")
  # 응답 처리 - post_router.py
  return post
# user_in 은 작성자 혹은 게시글임
  

# Upadate: 게시글 수정 - PUT, 제목과 내용만 가능
# 응답 처리 - post_router.py
@router.put("/{post_id}", response_model=PostResponse)
# 요청 처리 - post_router.py
def update_post(post_id: int, user_in: PostUpdate, db: Session = Depends(get_db)):
  # 비즈니스 로직 - post_service.py
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  
  if user_in.title is not None: 
    post.title = user_in.title
  if user_in.content is not None:
    post.content = user_in.content

  # DB 접근 - post_repository.py
  db.commit()
  db.refresh(post)
  # 응답 처리 - post_router.py
  return post

# Delete: 게시글 삭제 - DELETE
# response_model 없음
# 응답 처리 - post_router.py
@router.delete("/{post_id}", status_code=204)
# 요청 처리 - post_router.py
def delete_post(post_id: int, db: Session = Depends(get_db)): #받는 정보는 id임
  # 비즈니스 로직 - post_service.py
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post: 
    raise HTTPException(status_code=404, details="게시물을 찾을 수 없습니다.")
  
  # DB 접근 - post_repository.py
  db.delete(post)
  db.commit
