from typing import Dict, Any


class FormatAnalyzer:
    KEY_SECTIONS = ["objective", "experience", "projects", "skills", "education"]

    @classmethod
    def analyze(cls, text: str, sections: Dict[str, str]) -> Dict[str, Any]:
        """
        Đánh giá cấu trúc, bố cục và tính cân đối của văn bản CV (Tối đa 5đ).
        """
        words = text.split()
        word_count = len(words)

        # 1. Số lượng section cốt lõi có trong CV (Tối đa 2.5đ)
        found_sections = [sec for sec in cls.KEY_SECTIONS if sections.get(sec, "").strip()]
        sec_ratio = len(found_sections) / len(cls.KEY_SECTIONS)
        sec_score = round(sec_ratio * 2.5, 1)

        # 2. Độ dài văn bản hợp lý (Tối đa 2.5đ)
        # Quá ngắn (< 150 từ): 0.5đ
        # Hơi ngắn (150 - 300 từ): 1.5đ
        # Chuẩn (300 - 1500 từ): 2.5đ
        # Quá dài (> 2000 từ): 1.5đ
        if 300 <= word_count <= 1600:
            len_score = 2.5
            len_status = "Độ dài tiêu chuẩn, dễ theo dõi"
        elif 150 <= word_count < 300:
            len_score = 1.5
            len_status = "Hơi ngắn, nên bổ sung chi tiết"
        elif word_count > 1600:
            len_score = 1.5
            len_status = "Hơi dài, nên cô đọng trọng tâm"
        else:
            len_score = 0.5
            len_status = "Quá ngắn, thiếu thông tin cốt lõi"

        total_score = min(sec_score + len_score, 5.0)

        return {
            "score": total_score,
            "wordCount": word_count,
            "sectionsFound": found_sections,
            "details": {
                "sectionCompleteness": f"{len(found_sections)}/{len(cls.KEY_SECTIONS)} mục chính",
                "lengthStatus": len_status
            }
        }
