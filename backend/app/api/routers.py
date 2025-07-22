from fastapi import APIRouter
from app.api.controller.analyze import router as analyze_router
from app.api.controller.generate import router as generate_router

router = APIRouter()
router.include_router(analyze_router)
router.include_router(generate_router)