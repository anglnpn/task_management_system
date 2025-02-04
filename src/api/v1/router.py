from fastapi import APIRouter

from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.job import router as job_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(job_router, prefix="/job", tags=["Job"])
