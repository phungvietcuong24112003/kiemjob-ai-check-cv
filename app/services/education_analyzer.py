import re
from typing import Dict, Any


class EducationAnalyzer:
    DEGREE_PATTERNS = {
        "tien_si": ["tiến sĩ", "ph.d", "phd", "doctorate"],
        "thac_si": ["thạc sĩ", "master", "m.sc", "mba"],
        "dai_hoc": ["đại học", "cử nhân", "kỹ sư", "bachelor", "b.s", "b.a", "engineer"],
        "cao_dang": ["cao đẳng", "associate degree", "college"],
        "trung_cap": ["trung cấp", "nghề", "vocational"]
    }

    UNIVERSITIES = [
        "bách khoa", "quốc gia", "kinh tế quốc dân", "ngoại thương", "fpt", "công nghệ",
        "khoa học tự nhiên", "kinh tế", "ngân hàng", "học viện", "sư phạm kỹ thuật",
        "bưu chính viễn thông", "hust", "neu", "ftu", "uet", "uit", "vnu", "hutech",
        "hoa sen", "tôn đức thắng", "giao thông vận tải"
    ]

    @classmethod
    def analyze(cls, text: str, edu_section_text: str = "") -> Dict[str, Any]:
        """
        Phân tích học vấn (Tối đa 10đ).
        """
        scan_text = edu_section_text if edu_section_text.strip() else text
        low_scan = scan_text.lower()

        # 1. Trình độ học vấn cao nhất
        matched_level = "dai_hoc"  # Default
        highest_score = 0
        level_scores = {"tien_si": 5, "thac_si": 4, "dai_hoc": 3, "cao_dang": 2, "trung_cap": 1}

        for lvl, patterns in cls.DEGREE_PATTERNS.items():
            for pat in patterns:
                if re.search(r"\b" + re.escape(pat) + r"\b", low_scan):
                    if level_scores.get(lvl, 0) > highest_score:
                        highest_score = level_scores[lvl]
                        matched_level = lvl
                    break

        # 2. Tên trường / Cơ sở đào tạo
        matched_uni = None
        for uni in cls.UNIVERSITIES:
            if uni in low_scan:
                matched_uni = uni.title()
                break

        # 3. Tính điểm học vấn (Tối đa 10đ):
        # - Nhận diện trình độ học vấn: 4.0đ
        # - Nhận diện trường đào tạo: 3.0đ
        # - Có chuyên ngành / năm tốt nghiệp: 3.0đ
        score = 0.0
        details = {}

        if highest_score > 0 or edu_section_text:
            score += 4.0
            details["levelRecognized"] = True
        else:
            details["levelRecognized"] = False

        if matched_uni:
            score += 3.0
            details["universityFound"] = matched_uni
        elif edu_section_text:
            score += 1.5
            details["universityFound"] = "Có trường nhưng chưa định danh"
        else:
            details["universityFound"] = "Không rõ"

        # Chuyên ngành & năm
        has_major_or_year = any(k in low_scan for k in ["chuyên ngành", "khoa", "ngành", "gpa", "tốt nghiệp", "năm", "major", "grade"]) or bool(re.search(r"\b20\d{2}\b", scan_text))
        if has_major_or_year:
            score += 3.0
            details["majorOrYearSpecified"] = True
        else:
            score += 1.0 if edu_section_text else 0.0
            details["majorOrYearSpecified"] = False

        return {
            "score": min(score, 10.0),
            "educationLevel": matched_level,
            "university": matched_uni,
            "details": details
        }
