from fastapi import APIRouter
from app.schemas.cv_schema import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse()


@router.get("/")
def root():
    return {
        "service": "ai-service-check-cv",
        "description": "KiemJob CV Analysis & Scoring Microservice",
        "status": "UP"
    }
