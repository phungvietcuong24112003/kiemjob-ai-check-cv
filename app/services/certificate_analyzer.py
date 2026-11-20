import re
from typing import Dict, Any, List


class CertificateAnalyzer:
    CERTIFICATES = [
        "ielts", "toeic", "toefl", "jlpt", "hsk", "topik",
        "aws", "aws certified", "azure", "gcp", "google cloud certified",
        "cisco", "ccna", "ccnp", "pmp", "scrum master", "psm", "pmi",
        "cpa", "acca", "cfa", "misa", "mos", "icaew", "oracle certified",
        "comptia", "istqb", "ckad", "cka"
    ]

    AWARDS = [
        "giải nhất", "giải nhì", "giải ba", "giải khuyến khích", "thủ khoa", "á khoa",
        "học bổng", "scholarship", "hackathon", "nhân viên xuất sắc", "top performer",
        "first prize", "second prize", "champion", "winner"
    ]

    @classmethod
    def analyze(cls, text: str, cert_section_text: str = "") -> Dict[str, Any]:
        """
        Phân tích chứng chỉ & thành tích (Tối đa 5đ, điểm thưởng khuyến khích).
        """
        scan_text = cert_section_text if cert_section_text.strip() else text
        low_scan = scan_text.lower()

        found_certs: List[str] = []
        for cert in cls.CERTIFICATES:
            if re.search(r"\b" + re.escape(cert) + r"\b", low_scan):
                found_certs.append(cert.upper())

        found_awards: List[str] = []
        for aw in cls.AWARDS:
            if aw in low_scan:
                found_awards.append(aw.title())

        # Điểm (Tối đa 5.0đ):
        # - Có chứng chỉ chuyên môn / ngoại ngữ: tối đa 3.5đ (mỗi cert +1.5đ)
        # - Có giải thưởng / thành tích / học bổng: tối đa 2.0đ (mỗi award +1.0đ)
        score = 0.0
        details = {}

        cert_score = min(len(found_certs) * 1.5, 3.5)
        award_score = min(len(found_awards) * 1.0, 2.0)

        score = cert_score + award_score
        details["certCount"] = len(found_certs)
        details["awardCount"] = len(found_awards)

        return {
            "score": min(score, 5.0),
            "certificates": found_certs[:6],
            "awards": found_awards[:4],
            "details": details
        }
