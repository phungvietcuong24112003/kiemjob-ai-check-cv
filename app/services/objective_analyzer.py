import re
from typing import Dict, Any


class ObjectiveAnalyzer:
    CAREER_KEYWORDS = [
        "mục tiêu", "định hướng", "phát triển", "cống hiến", "đóng góp",
        "học hỏi", "nâng cao", "chuyên môn", "kinh nghiệm", "kỹ năng",
        "thành công", "cơ hội", "trách nhiệm", "kết quả", "giá trị",
        "objective", "career", "growth", "contribute", "improve", "develop"
    ]

    @classmethod
    def analyze(cls, text: str, objective_text: str = "") -> Dict[str, Any]:
        """
        Phân tích mục tiêu nghề nghiệp / giới thiệu bản thân (Tối đa 10đ).
        """
        # Nếu đã tách được section objective thì dùng, nếu không tìm các đoạn đầu có chứa keyword
        target_text = objective_text.strip()
        if not target_text:
            lines = text[:800].splitlines()
            captured = []
            capturing = False
            for line in lines:
                low = line.lower()
                if any(k in low for k in ["mục tiêu nghề nghiệp", "giới thiệu bản thân", "career objective", "about me", "summary"]):
                    capturing = True
                    continue
                if capturing:
                    if len(line.strip()) < 50 and any(k in low for k in ["học vấn", "kinh nghiệm", "kỹ năng", "dự án", "education", "skills"]):
                        break
                    captured.append(line)
            target_text = "\n".join(captured).strip()

        words = target_text.split()
        word_count = len(words)

        score = 0.0
        details = {}

        if word_count >= 10:
            # 1. Có phần giới thiệu / mục tiêu: 4.0đ
            score += 4.0
            details["hasObjective"] = True

            # 2. Độ dài hợp lý (từ 25 đến 180 từ): 3.0đ (nếu 10-24 từ thì 1.5đ)
            if 25 <= word_count <= 200:
                score += 3.0
                details["lengthQuality"] = "Tốt"
            else:
                score += 1.5
                details["lengthQuality"] = "Hơi ngắn" if word_count < 25 else "Hơi dài"

            # 3. Chứa từ khóa định hướng giá trị / nghề nghiệp: 3.0đ
            matched_keywords = [k for k in cls.CAREER_KEYWORDS if k in target_text.lower()]
            if len(matched_keywords) >= 3:
                score += 3.0
                details["keywordsStrength"] = "Mạnh"
            elif len(matched_keywords) >= 1:
                score += 1.5
                details["keywordsStrength"] = "Trung bình"
            else:
                details["keywordsStrength"] = "Yếu"
        else:
            details["hasObjective"] = False
            details["lengthQuality"] = "Thiếu hoặc quá ngắn"
            details["keywordsStrength"] = "Không có"

        return {
            "score": min(score, 10.0),
            "wordCount": word_count,
            "text": target_text[:300] if target_text else "",
            "details": details
        }
