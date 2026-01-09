from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title="OSINT Dashboard API",
    description="API for OSINT investigation case management",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "message": "OSINT Dashboard API",
        "version": "0.1.0",
        "docs": "/docs",
    }


# Module routers will be added here as they are created
# from app.modules.auth import router as auth_router
# from app.modules.cases import router as cases_router
# app.include_router(auth_router, prefix="/api/v1")
# app.include_router(cases_router, prefix="/api/v1")
