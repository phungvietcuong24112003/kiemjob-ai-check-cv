from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "ai-service-check-cv"
    API_V1_STR: str = "/api/v1"
    ALGORITHM_VERSION: str = "v1-python-rule-based"
    ENVIRONMENT: str = "development"
    
    # Secret Key dùng để xác thực các request từ Spring Boot
    INTERNAL_SECRET_KEY: str = "kiemjob_internal_secret_change_in_prod"
    
    # CORS Origins
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
