import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.routes.health_routes import router as health_router
from app.routes.cv_routes import router as cv_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ai-service-check-cv")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Service Check CV khởi động thành công.")
    logger.info(f"Môi trường: {settings.ENVIRONMENT}")
    logger.info(f"Phiên bản thuật toán: {settings.ALGORITHM_VERSION}")
    yield
    logger.info("AI Service Check CV đang tắt.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservice phân tích và chấm điểm CV theo thang điểm 100 cho KiemJob",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phục vụ các file PDF CV mẫu cục bộ (hỗ trợ test URL trên localhost)
samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_cvs")
if os.path.exists(samples_dir):
    app.mount("/samples", StaticFiles(directory=samples_dir), name="samples")

# Đăng ký các router
app.include_router(health_router)
app.include_router(cv_router)
