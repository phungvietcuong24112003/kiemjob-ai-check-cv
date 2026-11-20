import re
from typing import Dict, Any, List


class ProjectAnalyzer:
    # Số liệu định lượng: %, x người dùng, doanh số, triệu/tỷ, KPI, tối ưu thời gian...
    METRIC_PATTERNS = [
        re.compile(r"\b\d+(?:\.\d+)?\s*%", re.IGNORECASE),
        re.compile(r"\b\d+\s*(?:người dùng|user|users|khách hàng|clients)\b", re.IGNORECASE),
        re.compile(r"\b\d+\s*(?:requests?/s|rps|tps|qps)\b", re.IGNORECASE),
        re.compile(r"\b(?:tăng|giảm|tiết kiệm|tối ưu)\s*\d+", re.IGNORECASE),
        re.compile(r"\b\d+\s*(?:triệu|tỷ|usd|\$|vnd)\b", re.IGNORECASE),
        re.compile(r"\b(?:đạt|vượt)\s*\d+\s*kpi\b", re.IGNORECASE),
        re.compile(r"\b\d+\s*(?:star|forks?|downloads?)\b", re.IGNORECASE),
    ]

    PROJECT_INDICATORS = [
        "dự án", "project", "hệ thống", "ứng dụng", "website", "platform", "portal",
        "phần mềm", "app", "service", "microservice", "dashboard"
    ]

    @classmethod
    def analyze(cls, text: str, project_section_text: str = "") -> Dict[str, Any]:
        """
        Phân tích dự án thực tế (Tối đa 20đ).
        """
        scan_text = project_section_text if project_section_text.strip() else text
        low_scan = scan_text.lower()

        # 1. Nhận diện các dự án (Có từ chỉ dự án hoặc section project)
        has_project_sec = bool(project_section_text and len(project_section_text.strip()) > 30)
        found_indicators = [ind for ind in cls.PROJECT_INDICATORS if ind in low_scan]

        # 2. Nhận diện số liệu định lượng (Metrics)
        metrics_found: List[str] = []
        for pat in cls.METRIC_PATTERNS:
            matches = pat.findall(scan_text)
            for m in matches:
                if m not in metrics_found:
                    metrics_found.append(m)

        # 3. Tính điểm dự án (Tối đa 20đ):
        # - Có danh mục dự án rõ ràng: 5.0đ
        # - Nêu công nghệ & công cụ dùng trong dự án: 5.0đ
        # - Mô tả vai trò & trách nhiệm cá nhân: 5.0đ
        # - Có số liệu định lượng kết quả (%/số lượng): 5.0đ
        score = 0.0
        details = {}

        # Có dự án
        if has_project_sec or len(found_indicators) >= 2:
            proj_score = 5.0
            details["hasProjects"] = True
        elif len(found_indicators) >= 1:
            proj_score = 3.0
            details["hasProjects"] = "Đề cập ít"
        else:
            proj_score = 0.0
            details["hasProjects"] = False
        score += proj_score

        # Công nghệ trong dự án
        has_tech = any(k in low_scan for k in ["công nghệ", "tech stack", "technologies", "sử dụng", "ngôn ngữ", "database", "framework"])
        if has_tech or proj_score >= 3.0:
            tech_score = 5.0
            details["techStackSpecified"] = True
        else:
            tech_score = 2.0
            details["techStackSpecified"] = False
        score += tech_score

        # Vai trò trong dự án
        has_role = any(k in low_scan for k in ["vai trò", "role", "trách nhiệm", "nhiệm vụ", "responsibilities", "thành viên", "trưởng nhóm"])
        if has_role:
            role_score = 5.0
            details["roleSpecified"] = True
        else:
            role_score = 2.5 if proj_score >= 3.0 else 0.0
            details["roleSpecified"] = False
        score += role_score

        # Số liệu định lượng
        metrics_count = len(metrics_found)
        if metrics_count >= 3:
            metric_score = 5.0
            details["metricsQuality"] = "Xuất sắc (nhiều số liệu)"
        elif metrics_count >= 1:
            metric_score = 3.5
            details["metricsQuality"] = "Tốt (có số liệu)"
        else:
            metric_score = 0.0
            details["metricsQuality"] = "Thiếu số liệu định lượng"
        score += metric_score

        return {
            "score": min(score, 20.0),
            "metricsFound": metrics_found[:10],
            "metricsCount": metrics_count,
            "details": details
        }
