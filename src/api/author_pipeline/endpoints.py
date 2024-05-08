from fastapi import APIRouter
from . import pipeline

router = APIRouter()
router.include_router(pipeline.router, tags=["author_pipeline"])