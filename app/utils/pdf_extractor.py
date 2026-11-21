import io
import logging
from typing import Tuple
from pypdf import PdfReader

logger = logging.getLogger("ai-service-check-cv.pdf")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class PdfExtractionError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PdfExtractor:
    @classmethod
    def extract_text_from_bytes(cls, file_bytes: bytes, filename: str = "upload.pdf") -> str:
        """
        Trích xuất văn bản từ binary của file PDF hoàn toàn trong bộ nhớ (In-memory).
        Kiểm tra tính hợp lệ, dung lượng và các trường hợp lỗi thường gặp.
        """
        # 1. Kiểm tra dung lượng
        if not file_bytes or len(file_bytes) == 0:
            raise PdfExtractionError("File gửi lên rỗng hoặc không có dữ liệu", status_code=400)

        if len(file_bytes) > MAX_FILE_SIZE:
            raise PdfExtractionError("Dung lượng file vượt quá giới hạn tối đa cho phép (10MB)", status_code=400)

        # 2. Kiểm tra magic bytes (%PDF) để tránh giả mạo extension
        if not file_bytes.startswith(b"%PDF"):
            raise PdfExtractionError("Định dạng file không hợp lệ. Chỉ chấp nhận tài liệu PDF tiêu chuẩn", status_code=400)

        # 3. Đọc PDF bằng pypdf
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
        except Exception as e:
            logger.warning(f"Lỗi cú pháp file PDF {filename}: {str(e)}")
            raise PdfExtractionError("Không thể đọc cấu trúc file PDF. File có thể bị hỏng", status_code=400)

        # 4. Kiểm tra mã hóa / mật khẩu
        if reader.is_encrypted:
            try:
                # Thử giải mã với mật khẩu rỗng
                decrypted = reader.decrypt("")
                if decrypted == 0:
                    raise PdfExtractionError("File PDF đã bị khóa mật khẩu, hệ thống không thể phân tích", status_code=400)
            except Exception:
                raise PdfExtractionError("File PDF đã bị khóa mật khẩu hoặc có cơ chế bảo vệ quyền đọc", status_code=400)

        # 5. Trích xuất text từ tất cả các trang
        extracted_pages = []
        try:
            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(page_text.strip())
        except Exception as e:
            logger.warning(f"Lỗi trích xuất trang PDF: {str(e)}")
            raise PdfExtractionError("Lỗi trong quá trình trích xuất văn bản từ các trang PDF", status_code=400)

        full_text = "\n\n".join(extracted_pages).strip()

        # 6. Kiểm tra trường hợp PDF ảnh scan (không có text layer)
        if len(full_text) < 30:
            raise PdfExtractionError(
                "File PDF không chứa văn bản có thể trích xuất (tài liệu scan hoặc chứa toàn hình ảnh). "
                "Vui lòng tải lên file PDF có lớp văn bản (text-based).",
                status_code=400
            )

        return full_text
