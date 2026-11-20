import re
import unicodedata
from typing import Dict, List, Tuple


class TextCleaner:
    SECTION_KEYWORDS = {
        "objective": [
            "mục tiêu nghề nghiệp", "mục tiêu", "giới thiệu", "giới thiệu bản thân",
            "tóm tắt", "career objective", "objective", "summary", "about me", "professional summary"
        ],
        "experience": [
            "kinh nghiệm làm việc", "kinh nghiệm", "quá trình làm việc", "lịch sử làm việc",
            "work experience", "experience", "employment history", "professional experience"
        ],
        "projects": [
            "dự án", "dự án nổi bật", "dự án cá nhân", "dự án thực tế",
            "projects", "personal projects", "key projects", "academic projects"
        ],
        "skills": [
            "kỹ năng", "kỹ năng chuyên môn", "kỹ năng làm việc", "chuyên môn",
            "skills", "technical skills", "core competencies", "competencies"
        ],
        "education": [
            "học vấn", "trình độ học vấn", "bằng cấp", "quá trình học tập",
            "education", "academic background", "qualifications"
        ],
        "certificates": [
            "chứng chỉ", "chứng nhận", "khóa học", "bằng khen",
            "certificates", "certifications", "licenses", "awards", "honors"
        ]
    }

    @classmethod
    def clean(cls, text: str) -> str:
        if not text:
            return ""
        # 1. Unicode NFC
        text = unicodedata.normalize("NFC", text)

        # 2. Xóa các ký tự bullet point đặc biệt của PDF
        text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\uF0B7\uF0A7\uF0D8]", " - ", text)

        # 3. Chuẩn hóa khoảng trắng ngang (tab, non-breaking space)
        text = re.sub(r"[ \t\u00A0\u200B\u200E\u200F]+", " ", text)

        # 4. Giảm số dòng trống liên tiếp (tối đa 2 dòng trống)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @classmethod
    def split_sections(cls, text: str) -> Dict[str, str]:
        """
        Phân tách văn bản CV thành các đoạn ngữ nghĩa dựa trên tiêu đề section.
        """
        cleaned = cls.clean(text)
        lines = cleaned.splitlines()

        sections: Dict[str, List[str]] = {
            "header": [],
            "objective": [],
            "experience": [],
            "projects": [],
            "skills": [],
            "education": [],
            "certificates": [],
            "other": []
        }

        current_sec = "header"

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Kiểm tra xem dòng này có phải là tiêu đề section hay không
            # Tiêu chuẩn: ngắn (< 50 ký tự), có thể in hoa, khớp keyword
            low = line_str.lower().strip(":-• \t")
            matched_sec = None

            if len(line_str) <= 50:
                for sec_key, keywords in cls.SECTION_KEYWORDS.items():
                    for kw in keywords:
                        if low == kw or low.startswith(kw + ":") or low.startswith(kw + " -"):
                            matched_sec = sec_key
                            break
                    if matched_sec:
                        break

            if matched_sec:
                current_sec = matched_sec
                continue

            sections[current_sec].append(line_str)

        return {k: "\n".join(v) for k, v in sections.items()}
