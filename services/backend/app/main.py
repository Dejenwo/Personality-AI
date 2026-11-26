from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import get_settings
from app.database import SessionLocal, init_db
from app.seed import seed_if_needed


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_if_needed(db)
    finally:
        db.close()
    yield


settings = get_settings()
app = FastAPI(
    title="PersonalityDNA AI API",
    version="0.1.0",
    description="Deterministic personality intelligence API. Scoring is not performed by AI.",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"ok": True, "service": "personalitydna-api", "env": settings.app_env}


@app.get("/")
def root():
    return JSONResponse(
        {
            "name": "PersonalityDNA AI",
            "tagline": "Discover Yourself. Understand Others. Transform Your Life.",
            "docs": "/api/docs",
            "openapi": "/api/v1/openapi.json",
        }
    )
