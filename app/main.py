import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Đăng ký các router
app.include_router(health_router)
app.include_router(cv_router)
