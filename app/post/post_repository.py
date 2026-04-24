# Repository: DB 접근만 담당
from sqlalchemy.orm import Session
from app.post.post_model import Post

class PostRepository:
  def __init__(self, db: Session):
    self.db = db

  # create & update
  # db에 저장하는 로직
  def save(self, post: Post) -> None:
    self.db.add(post)
    self.db.commit()
    self.db.refresh(post)
    return post
  
  # read
  def find_all(self) -> list[Post]:
    return self.db.query(Post).all()
  
  def find_by_id(self, post_id: int) -> Post | None:
    return self.db.query(Post).filter(Post.id == post_id).first()

  # delete
  def delete(self, post: Post) -> None:
    self.db.delete(post)
    self.db.commit()
