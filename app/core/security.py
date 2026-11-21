from fastapi import Header
from typing import Optional


def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
):
    """
    Theo yêu cầu dự án demo: Không bắt buộc X-API-Key hoặc xác thực phức tạp.
    Spring Boot gọi trực tiếp POST /api/v1/analyze-cv.
    """
    return True
