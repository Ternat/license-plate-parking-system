from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import APIException, api_exception_handler, general_exception_handler
from app.api.v1.router import api_router
from app.models.database import engine, Base
import os
from app.utils.logger import logger


Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")


os.makedirs(settings.UPLOAD_RAW_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_ENHANCED_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DETECTION_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_CORRECTED_DIR, exist_ok=True)
os.makedirs("./logs", exist_ok=True)
os.makedirs("./weights", exist_ok=True)
logger.info("Required directories created successfully")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="UK License Plate Recognition (LPR) Parking System API",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", summary="API Root")
async def root():
    return {
        "message": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting UK LPR Parking System API...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )