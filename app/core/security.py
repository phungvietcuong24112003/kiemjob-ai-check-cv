from fastapi import Header, HTTPException, status
from app.core.config import settings


def verify_internal_secret(
    x_internal_secret: str = Header(None, alias="X-Internal-Secret")
):
    """
    Xác thực secret key giữa Spring Boot và Python AI Service.
    Nếu ở môi trường development hoặc secret khớp thì cho phép truy cập.
    """
    # Nếu không cấu hình secret (để trống) thì bỏ qua kiểm tra
    if not settings.INTERNAL_SECRET_KEY or settings.INTERNAL_SECRET_KEY == "kiemjob_internal_secret_change_in_prod":
        # Cho phép chạy linh hoạt ở dev
        if x_internal_secret == settings.INTERNAL_SECRET_KEY or settings.ENVIRONMENT == "development":
            return True

    if not x_internal_secret or x_internal_secret != settings.INTERNAL_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Truy cập bị từ chối: X-Internal-Secret không hợp lệ"
        )
    return True
