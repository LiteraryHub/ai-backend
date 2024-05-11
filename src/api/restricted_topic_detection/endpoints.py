from fastapi import APIRouter
from . import detect

router = APIRouter()
router.include_router(detect.router, tags=["restricted_topic_detection"])