from app.post.post_repository import PostRepository
from app.post.post_schema import PostCreate, PostResponse, PostUpdate
from app.post.post_model import Post
from fastapi import HTTPException

class PostService:
  def __init__(self, repo: PostRepository):
    self.repo = repo

  def create_post(self, request: PostCreate) -> Post: 
    post = Post(
      title = self.title,
      content = self.content,
      writer = self.writer,
    )
    return self.repo.save(post)
  
  def get_posts(self) -> list[Post]:
    return self.repo.find_all()
    
  def get_post(self, post_id: int) -> Post:
    post = self.repo.find_by_id(post_id)
    if not post:
      raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")
    return post
    
  def update_post(self, post_id: int, request: PostUpdate) -> Post:
    post = self.get_post(post_id)
    if request.name is not None:
        post.name = request.name
    if request.email is not None:
        post.email = request.email
    return self.repo.save(post)

  def delete_post(self, post_id: int) -> None:
    post = self.find_by_id(post_id)
    self.repo.delete(post)

