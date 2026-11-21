import re


class LanguageDetector:
    VIETNAMESE_MARKERS = [
        "và", "của", "tại", "kinh nghiệm", "kỹ năng", "học vấn", "mục tiêu",
        "dự án", "công ty", "chức vụ", "trình độ", "đại học", "thành tích"
    ]
    
    VI_ACCENTS_REGEX = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]")

    @classmethod
    def detect(cls, text: str) -> str:
        """
        Nhận diện ngôn ngữ chính của CV: 'vi' (tiếng Việt) hoặc 'en' (tiếng Anh).
        """
        if not text:
            return "vi"

        low_text = text.lower()
        
        # 1. Đếm ký tự dấu tiếng Việt
        accent_matches = cls.VI_ACCENTS_REGEX.findall(low_text)
        if len(accent_matches) > 15:
            return "vi"

        # 2. Đếm các từ vựng đặc trưng
        vi_count = sum(1 for w in cls.VIETNAMESE_MARKERS if f" {w} " in f" {low_text} ")
        if vi_count >= 2:
            return "vi"

        # Mặc định là en nếu ít dấu tiếng Việt và ít từ tiếng Việt
        return "en" if len(accent_matches) < 5 else "vi"
