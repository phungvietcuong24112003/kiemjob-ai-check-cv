import io
import ipaddress
import logging
import socket
from urllib.parse import urlparse
from typing import Tuple
import httpx
from app.core.config import settings

logger = logging.getLogger("ai-service-check-cv.downloader")


class PdfDownloadError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PdfDownloader:
    MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    @classmethod
    def validate_url_safety(cls, url: str) -> Tuple[bool, str]:
        """
        Kiểm tra an toàn URL và chống tấn công Server-Side Request Forgery (SSRF).
        Ở môi trường production: Bắt buộc HTTPS, chặn hoàn toàn localhost, IP mạng nội bộ và Cloud Metadata.
        Ở môi trường development: Cho phép HTTP/localhost để test các file PDF mẫu.
        """
        if not url or not isinstance(url, str):
            return False, "URL không được để trống"

        try:
            parsed = urlparse(url.strip())
        except Exception:
            return False, "Cấu trúc URL không hợp lệ"

        # 1. Kiểm tra giao thức (Protocol)
        is_dev = settings.ENVIRONMENT == "development" or settings.ALLOW_LOCAL_URLS_FOR_TEST
        allowed_schemes = ("https", "http") if is_dev else ("https",)

        if parsed.scheme.lower() not in allowed_schemes:
            if not is_dev and parsed.scheme.lower() == "http":
                return False, "Chỉ chấp nhận URL bảo mật qua giao thức HTTPS"
            return False, f"Giao thức '{parsed.scheme}' không được hỗ trợ. Chỉ chấp nhận HTTPS"

        hostname = parsed.hostname
        if not hostname:
            return False, "URL thiếu tên miền hoặc địa chỉ máy chủ"

        # Luôn chặn Cloud Metadata endpoint nguy hiểm (169.254.169.254)
        if hostname == "169.254.169.254" or "metadata.google.internal" in hostname.lower():
            return False, "Không cho phép truy cập địa chỉ Metadata máy chủ đám mây (Anti-SSRF)"

        # 2. Ở Production: Chặn các hostname và IP nội bộ
        if not is_dev:
            blocked_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
            if hostname.lower() in blocked_hosts:
                return False, "Không cho phép truy cập địa chỉ máy chủ cục bộ hoặc nội bộ (Anti-SSRF)"

            try:
                addr_info = socket.getaddrinfo(hostname, None)
                for entry in addr_info:
                    ip_str = entry[4][0]
                    ip_obj = ipaddress.ip_address(ip_str)
                    if (
                        ip_obj.is_private
                        or ip_obj.is_loopback
                        or ip_obj.is_link_local
                        or ip_obj.is_reserved
                        or ip_obj.is_multicast
                        or ip_str == "169.254.169.254"
                    ):
                        return False, "Không cho phép truy cập địa chỉ IP nội bộ hoặc Metadata máy chủ đám mây (Anti-SSRF)"
            except socket.gaierror:
                return False, f"Không thể phân giải địa chỉ tên miền: {hostname}"
            except Exception as e:
                return False, f"Lỗi khi kiểm tra địa chỉ máy chủ: {str(e)}"

        return True, ""

    @classmethod
    async def download_pdf(cls, url: str) -> bytes:
        """
        Tải file PDF từ URL an toàn, kiểm tra dung lượng và định dạng hoàn toàn trong bộ nhớ.
        Không lưu file ra ổ đĩa và không ghi URL vào log.
        """
        # 1. Kiểm tra an toàn SSRF
        is_safe, error_msg = cls.validate_url_safety(url)
        if not is_safe:
            raise PdfDownloadError(error_msg, status_code=400)

        # 2. Tải nhị phân có streaming và timeout
        timeout = httpx.Timeout(settings.DOWNLOAD_TIMEOUT_SECONDS, connect=10.0)
        chunks = []
        total_size = 0

        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
                async with client.stream("GET", url.strip()) as response:
                    # Kiểm tra mã trạng thái HTTP
                    if response.status_code in (401, 403):
                        raise PdfDownloadError(
                            "URL tải file PDF đã hết hạn hoặc không có quyền truy cập từ AWS S3 (HTTP 403/401)",
                            status_code=403
                        )
                    if response.status_code == 404:
                        raise PdfDownloadError(
                            "Không tìm thấy file PDF tại URL được cung cấp (HTTP 404 Not Found)",
                            status_code=404
                        )
                    if response.status_code >= 400:
                        raise PdfDownloadError(
                            f"Máy chủ lưu trữ file trả về lỗi khi tải (HTTP {response.status_code})",
                            status_code=400
                        )

                    # Kiểm tra Content-Length header nếu có
                    content_length = response.headers.get("content-length")
                    if content_length and content_length.isdigit():
                        if int(content_length) > cls.MAX_BYTES:
                            raise PdfDownloadError(
                                f"File PDF vượt quá dung lượng cho phép ({settings.MAX_FILE_SIZE_MB}MB)",
                                status_code=400
                            )

                    # Đọc từng chunk nhị phân để kiểm soát dung lượng thực tế
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        total_size += len(chunk)
                        if total_size > cls.MAX_BYTES:
                            raise PdfDownloadError(
                                f"File tải về vượt quá dung lượng tối đa cho phép ({settings.MAX_FILE_SIZE_MB}MB)",
                                status_code=400
                            )
                        chunks.append(chunk)

        except httpx.TimeoutException:
            raise PdfDownloadError(
                f"Quá thời gian tải file PDF từ URL (Timeout sau {settings.DOWNLOAD_TIMEOUT_SECONDS}s)",
                status_code=408
            )
        except httpx.RequestError as e:
            raise PdfDownloadError(
                f"Không thể kết nối đến URL tải file: {type(e).__name__}",
                status_code=400
            )

        file_bytes = b"".join(chunks)

        # 3. Kiểm tra file rỗng
        if len(file_bytes) == 0:
            raise PdfDownloadError("Dữ liệu tải về từ URL bị rỗng (0 bytes)", status_code=400)

        # 4. Kiểm tra Magic Bytes %PDF
        if not file_bytes.startswith(b"%PDF"):
            raise PdfDownloadError(
                "Nội dung tải về từ URL không phải là tài liệu PDF tiêu chuẩn (sai định dạng header %PDF)",
                status_code=400
            )

        return file_bytes
