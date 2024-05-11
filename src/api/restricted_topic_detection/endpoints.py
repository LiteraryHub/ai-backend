from fastapi import APIRouter
from . import restricted_topic_detection

router = APIRouter()
router.include_router(restricted_topic_detection.router, tags=["restricted_topic_detection"])