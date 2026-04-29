from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.post.post_service import PostService
from app.post.post_repository import PostRepository
from app.post.post_schema import PostResponse, PostCreate, PostUpdate

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])
# get post 

def get_post_service(db: Session = Depends(get_db)) -> PostService:
  return PostService(PostRepository(db))

@router.post("", response_model=PostResponse, status_code=201)
def create_post(request: PostCreate, post_service : PostService = Depends(get_post_service)):
  return post_service.create_post(request)

@router.get("", response_model=list[PostResponse])
def get_posts(post_service : PostService = Depends(get_post_service)):
  return post_service.get_posts()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, post_service : PostService = Depends(get_post_service)):
  return post_service.get_post(post_id)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, request: PostUpdate, post_service : PostService = Depends(get_post_service)):
  return post_service.update_post(post_id, request)

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, post_service : PostService = Depends(get_post_service)):
  post_service.delete_post(post_id)