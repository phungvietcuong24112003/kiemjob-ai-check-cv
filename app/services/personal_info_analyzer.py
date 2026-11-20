import re
from typing import Dict, Any, List, Optional
from app.services.text_cleaner import TextCleaner


class PersonalInfoAnalyzer:
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    )
    
    # Số điện thoại VN: bắt đầu bằng 0 hoặc +84, theo sau bởi 3,5,7,8,9 và 8 chữ số (cho phép dấu cách, chấm, gạch ngang)
    PHONE_PATTERN = re.compile(
        r"(?:\+?84|0)[35789](?:[\s.-]*\d){8}\b"
    )

    LINK_PATTERNS = [
        re.compile(r"https?://github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE),
        re.compile(r"https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_%-]+", re.IGNORECASE),
        re.compile(r"https?://gitlab\.com/[a-zA-Z0-9_-]+", re.IGNORECASE),
        re.compile(r"https?://(?:www\.)?(?:behance\.net|dribbble\.com)/[a-zA-Z0-9_-]+", re.IGNORECASE),
        re.compile(r"https?://[a-zA-Z0-9-]+\.(?:github\.io|dev|io|me|vn|com)(?:/[^\s]*)?", re.IGNORECASE),
    ]

    PROVINCES = [
        "Hà Nội", "Hồ Chí Minh", "TP.HCM", "TP HCM", "Sài Gòn", "Đà Nẵng",
        "Hải Phòng", "Cần Thơ", "Bình Dương", "Đồng Nai", "Bà Rịa - Vũng Tàu",
        "Bắc Ninh", "Vĩnh Phúc", "Huế", "Quảng Nam", "Nha Trang", "Khánh Hòa",
        "Lâm Đồng", "Đà Lạt", "Long An", "Tiền Giang", "Thái Nguyên", "Hải Dương"
    ]

    @classmethod
    def analyze(cls, text: str, header_text: str = "") -> Dict[str, Any]:
        """
        Phân tích thông tin cá nhân và trả về điểm số (tối đa 10đ) cùng dữ liệu trích xuất.
        """
        full_text = text
        scan_text = (header_text + "\n" + text[:1500]) if header_text else text[:1500]

        # 1. Trích xuất Email
        emails = cls.EMAIL_PATTERN.findall(scan_text)
        email = emails[0] if emails else None

        # 2. Trích xuất Số điện thoại
        phone_matches = cls.PHONE_PATTERN.findall(scan_text)
        phone = re.sub(r"[\s.-]", "", phone_matches[0]) if phone_matches else None

        # 3. Trích xuất Liên kết (GitHub, LinkedIn, Portfolio...)
        links: List[str] = []
        for pat in cls.LINK_PATTERNS:
            found = pat.findall(full_text)
            for f in found:
                if f not in links:
                    links.append(f)

        # 4. Trích xuất Địa điểm
        location: Optional[str] = None
        for prov in cls.PROVINCES:
            if re.search(r"\b" + re.escape(prov) + r"\b", scan_text, re.IGNORECASE):
                location = prov
                if prov in ["TP HCM", "TP.HCM", "Sài Gòn"]:
                    location = "Hồ Chí Minh"
                break

        # 5. Họ và tên (Dựa trên dòng đầu tiên của header hoặc phần đầu văn bản)
        full_name = cls._extract_name(header_text or text[:400])

        # 6. Tính điểm (Tối đa 10đ)
        # - Họ tên: 3.0đ
        # - Email: 3.0đ
        # - Số điện thoại: 3.0đ
        # - Link chuyên môn hoặc Địa chỉ: 1.0đ
        score = 0.0
        details = {}

        if full_name:
            score += 3.0
            details["fullNameValid"] = True
        else:
            details["fullNameValid"] = False

        if email:
            score += 3.0
            details["emailValid"] = True
        else:
            details["emailValid"] = False

        if phone:
            score += 3.0
            details["phoneValid"] = True
        else:
            details["phoneValid"] = False

        if links or location:
            score += 1.0
            details["linksOrLocationValid"] = True
        else:
            details["linksOrLocationValid"] = False

        return {
            "score": min(score, 10.0),
            "fullName": full_name,
            "email": email,
            "phone": phone,
            "location": location or "Chưa cập nhật",
            "links": links,
            "details": details
        }

    @classmethod
    def _extract_name(cls, text_block: str) -> Optional[str]:
        lines = [line.strip() for line in text_block.splitlines() if line.strip()]
        for line in lines[:5]:
            # Bỏ qua các dòng chứa nhãn như 'cv', 'hồ sơ', 'email', 'sđt', 'curriculum vitae'
            low = line.lower()
            if any(k in low for k in ["curriculum vitae", "hồ sơ xin việc", "cv xin việc", "resume", "thông tin cá nhân"]):
                continue
            if "@" in line or any(c.isdigit() for c in line):
                continue
            # Họ tên tiếng Việt thường 2-5 từ, chữ cái đầu viết hoa
            words = line.split()
            if 2 <= len(words) <= 5 and all(w[0].isupper() or w[0].isalpha() for w in words):
                return line
        return lines[0] if lines and len(lines[0].split()) <= 5 else None
