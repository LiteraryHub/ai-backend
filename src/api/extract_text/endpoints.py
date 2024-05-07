from fastapi import APIRouter
from . import extract_text

router = APIRouter()
router.include_router(extract_text.router, tags=["extract_text"])