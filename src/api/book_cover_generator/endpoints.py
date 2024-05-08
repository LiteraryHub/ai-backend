from fastapi import APIRouter
from . import book_cover_generator

router = APIRouter()
# router.include_router(book_cover_generator.router, tags=["book_cover_generator"])