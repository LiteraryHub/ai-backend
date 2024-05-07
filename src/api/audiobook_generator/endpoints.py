from fastapi import APIRouter
from . import audiobook

router = APIRouter()

# Include the audiobook router in the main router
router.include_router(audiobook.router, tags=["audiobook_generator"])