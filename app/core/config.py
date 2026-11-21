from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "ai-service-check-cv"
    API_V1_STR: str = "/api/v1"
    ALGORITHM_VERSION: str = "v1"
    ENVIRONMENT: str = "development"
    
    # API Key (Tùy chọn cho dự án demo)
    API_KEY: str = "kiemjob_secret_key_change_in_prod"
    INTERNAL_SECRET_KEY: str = "kiemjob_secret_key_change_in_prod"

    # Giới hạn kích thước file tải xuống (10MB)
    MAX_FILE_SIZE_MB: int = 10
    
    # Timeout khi tải file PDF từ URL (giây)
    DOWNLOAD_TIMEOUT_SECONDS: int = 20
    
    # Cho phép HTTP hoặc local URL (bật ở development để test local sample PDF)
    ALLOW_LOCAL_URLS_FOR_TEST: bool = True
    
    # CORS Origins
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
