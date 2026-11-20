import re
from datetime import datetime
from typing import Dict, Any, List, Tuple


class ExperienceAnalyzer:
    DATE_RANGE_PATTERN = re.compile(
        r"(\b(?:0?[1-9]|1[0-2])[\/\.-]?(?:20\d{2}|19\d{2})|\b(?:20\d{2}|19\d{2}))\s*[-–—tođến\s]+\s*(\b(?:0?[1-9]|1[0-2])[\/\.-]?(?:20\d{2}|19\d{2})|\b(?:20\d{2}|19\d{2})|hiện tại|present|nay)\b",
        re.IGNORECASE
    )

    JOB_TITLES = [
        "developer", "lập trình viên", "kỹ sư", "engineer", "chuyên viên",
        "trưởng nhóm", "team lead", "tech lead", "quản lý", "manager",
        "kế toán", "nhân viên kinh doanh", "sales", "marketing", "designer",
        "tester", "qa", "qc", "ba", "business analyst", "intern", "thực tập sinh"
    ]

    SENIORITY_KEYWORDS = {
        "intern": ["intern", "thực tập sinh", "trainee"],
        "fresher": ["fresher", "mới tốt nghiệp"],
        "junior": ["junior", "1 năm", "2 năm"],
        "senior": ["senior", "chuyên viên cao cấp", "lead", "trưởng nhóm"],
        "manager": ["manager", "trưởng phòng", "giám đốc", "director"]
    }

    @classmethod
    def analyze(cls, text: str, exp_section_text: str = "") -> Dict[str, Any]:
        """
        Phân tích kinh nghiệm làm việc (Tối đa 20đ).
        """
        target_text = exp_section_text if exp_section_text.strip() else text
        low_target = target_text.lower()

        # 1. Tìm các khoảng thời gian làm việc
        date_matches = cls.DATE_RANGE_PATTERN.findall(target_text)
        total_months = cls._calculate_total_months(date_matches)
        years = round(total_months / 12.0, 1)

        # 2. Nhận diện các chức danh từng đảm nhiệm
        detected_titles = []
        for title in cls.JOB_TITLES:
            if re.search(r"\b" + re.escape(title) + r"\b", low_target):
                detected_titles.append(title.title())

        # 3. Nhận diện cấp bậc (Seniority)
        seniority = "mid-level"
        if years < 0.5:
            seniority = "fresher" if "fresher" in low_target else "intern"
        elif years < 2.0:
            seniority = "junior"
        elif years >= 5.0:
            seniority = "senior"

        # 4. Tính điểm kinh nghiệm (Tối đa 20đ)
        # - Có khoảng thời gian rõ ràng: 5.0đ
        # - Có chức danh / vị trí công việc: 5.0đ
        # - Chi tiết mô tả nhiệm vụ (độ dài text và gạch đầu dòng): 5.0đ
        # - Tính liên tục & số năm tích lũy: 5.0đ
        score = 0.0
        details = {}

        # Mốc thời gian
        if date_matches:
            time_score = 5.0
            details["timeRangesFound"] = len(date_matches)
        else:
            time_score = 2.0 if years > 0 else 0.0
            details["timeRangesFound"] = 0
        score += time_score

        # Vị trí công việc
        if detected_titles:
            title_score = 5.0
            details["titlesCount"] = len(detected_titles)
        else:
            title_score = 1.5 if exp_section_text else 0.0
            details["titlesCount"] = 0
        score += title_score

        # Độ chi tiết mô tả nhiệm vụ
        word_count = len(target_text.split())
        if word_count >= 150:
            desc_score = 5.0
        elif word_count >= 60:
            desc_score = 3.5
        elif word_count >= 20:
            desc_score = 2.0
        else:
            desc_score = 0.0
        score += desc_score
        details["descriptionDetail"] = "Chi tiết" if desc_score == 5.0 else "Ngắn gọn"

        # Số năm tích lũy
        if years >= 3.0:
            year_score = 5.0
        elif years >= 1.0:
            year_score = 4.0
        elif years >= 0.5:
            year_score = 3.0
        elif years > 0:
            year_score = 2.0
        else:
            year_score = 1.0 if exp_section_text else 0.0
        score += year_score
        details["yearsScore"] = year_score

        return {
            "score": min(score, 20.0),
            "yearsExperience": years,
            "seniority": seniority,
            "jobTitles": detected_titles[:5],
            "details": details
        }

    @classmethod
    def _calculate_total_months(cls, matches: List[Tuple[str, str]]) -> int:
        if not matches:
            return 0
        total = 0
        current_year = datetime.now().year

        for start_str, end_str in matches:
            try:
                sy = cls._parse_year(start_str)
                if not sy:
                    continue
                if any(k in end_str.lower() for k in ["hiện tại", "present", "nay"]):
                    ey = current_year
                else:
                    ey = cls._parse_year(end_str) or current_year

                diff = (ey - sy) * 12
                if diff > 0:
                    total += min(diff, 120)  # Giới hạn tối đa 10 năm cho 1 mốc
            except Exception:
                continue

        return min(total, 360)

    @classmethod
    def _parse_year(cls, s: str) -> int:
        digits = re.findall(r"\b(20\d{2}|19\d{2})\b", s)
        return int(digits[0]) if digits else None
