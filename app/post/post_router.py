from fastapi import APIRouter, Depends


router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])
# get post 