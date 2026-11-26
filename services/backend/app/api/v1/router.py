from fastapi import APIRouter, Depends

from app.api.v1.auth import router as auth_router
from app.api.v1.services import router as services_router
from app.rate_limit import rate_limit

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, dependencies=[Depends(rate_limit("auth"))])
api_router.include_router(services_router, dependencies=[Depends(rate_limit("default"))])
