from typing import Dict, Any
from app.schemas.cv_schema import ScoringDetail, ScoringItem


class ScoreCalculator:
    MAX_SCORES = {
        "personal_info": 10.0,
        "introduction": 10.0,
        "skills": 20.0,
        "experience": 20.0,
        "projects": 20.0,
        "education": 10.0,
        "certificates": 5.0,
        "format": 5.0
    }

    @classmethod
    def calculate_total(
        cls,
        personal_info: Dict[str, Any],
        objective: Dict[str, Any],
        skills: Dict[str, Any],
        experience: Dict[str, Any],
        projects: Dict[str, Any],
        education: Dict[str, Any],
        certificates: Dict[str, Any],
        format_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Tính điểm tổng và chuẩn hóa điểm từng phần theo thang 100.
        Đảm bảo:
        - Tổng điểm các phần chính xác bằng điểm tổng (0 - 100).
        - Mỗi phần có score, maxScore và reason cụ thể.
        """
        p_score = min(float(personal_info.get("score", 0.0)), cls.MAX_SCORES["personal_info"])
        o_score = min(float(objective.get("score", 0.0)), cls.MAX_SCORES["introduction"])
        s_score = min(float(skills.get("score", 0.0)), cls.MAX_SCORES["skills"])
        e_score = min(float(experience.get("score", 0.0)), cls.MAX_SCORES["experience"])
        proj_score = min(float(projects.get("score", 0.0)), cls.MAX_SCORES["projects"])
        edu_score = min(float(education.get("score", 0.0)), cls.MAX_SCORES["education"])
        cert_score = min(float(certificates.get("score", 0.0)), cls.MAX_SCORES["certificates"])
        f_score = min(float(format_info.get("score", 0.0)), cls.MAX_SCORES["format"])

        # Làm tròn 1 chữ số thập phân
        p_score = round(p_score, 1)
        o_score = round(o_score, 1)
        s_score = round(s_score, 1)
        e_score = round(e_score, 1)
        proj_score = round(proj_score, 1)
        edu_score = round(edu_score, 1)
        cert_score = round(cert_score, 1)
        f_score = round(f_score, 1)

        total = round(p_score + o_score + s_score + e_score + proj_score + edu_score + cert_score + f_score, 1)
        total = min(max(total, 0.0), 100.0)

        # Xây dựng lý do (Reasons)
        p_reason = personal_info.get("reason") or cls._default_personal_reason(p_score, personal_info)
        o_reason = objective.get("reason") or cls._default_objective_reason(o_score, objective)
        s_reason = skills.get("reason") or cls._default_skills_reason(s_score, skills)
        e_reason = experience.get("reason") or cls._default_exp_reason(e_score, experience)
        proj_reason = projects.get("reason") or cls._default_proj_reason(proj_score, projects)
        edu_reason = education.get("reason") or cls._default_edu_reason(edu_score, education)
        cert_reason = certificates.get("reason") or cls._default_cert_reason(cert_score, certificates)
        f_reason = format_info.get("reason") or cls._default_format_reason(f_score, format_info)

        scoring_detail = ScoringDetail(
            personalInfo=ScoringItem(score=p_score, maxScore=cls.MAX_SCORES["personal_info"], reason=p_reason),
            introduction=ScoringItem(score=o_score, maxScore=cls.MAX_SCORES["introduction"], reason=o_reason),
            skills=ScoringItem(score=s_score, maxScore=cls.MAX_SCORES["skills"], reason=s_reason),
            experience=ScoringItem(score=e_score, maxScore=cls.MAX_SCORES["experience"], reason=e_reason),
            projects=ScoringItem(score=proj_score, maxScore=cls.MAX_SCORES["projects"], reason=proj_reason),
            education=ScoringItem(score=edu_score, maxScore=cls.MAX_SCORES["education"], reason=edu_reason),
            certificates=ScoringItem(score=cert_score, maxScore=cls.MAX_SCORES["certificates"], reason=cert_reason),
            format=ScoringItem(score=f_score, maxScore=cls.MAX_SCORES["format"], reason=f_reason)
        )

        return {
            "qualityScore": total,
            "scoring": scoring_detail
        }

    @staticmethod
    def _default_personal_reason(score: float, data: Dict[str, Any]) -> str:
        if score >= 9.0:
            return "Thông tin liên hệ đầy đủ (họ tên, email, số điện thoại, liên kết chuyên môn/địa chỉ)"
        elif score >= 6.0:
            missing = []
            if not data.get("phone"):
                missing.append("số điện thoại")
            if not data.get("email"):
                missing.append("email")
            if not data.get("links"):
                missing.append("link LinkedIn/GitHub")
            return f"Thông tin cơ bản nhưng còn thiếu: {', '.join(missing) if missing else 'liên kết chuyên môn'}"
        return "Thông tin cá nhân và liên hệ còn sơ sài, thiếu phương thức liên lạc chính thức"

    @staticmethod
    def _default_objective_reason(score: float, data: Dict[str, Any]) -> str:
        if score >= 9.0:
            return "Mục tiêu nghề nghiệp rõ ràng, nêu bật định hướng phát triển và giá trị đóng góp"
        elif score >= 5.0:
            return "Có phần giới thiệu bản thân nhưng còn ngắn hoặc chưa làm nổi bật thế mạnh chuyên môn"
        return "Chưa có phần giới thiệu hoặc mục tiêu nghề nghiệp còn quá ngắn"

    @staticmethod
    def _default_skills_reason(score: float, data: Dict[str, Any]) -> str:
        count = len(data.get("skills", []))
        if score >= 18.0:
            return f"Kỹ năng chuyên môn phong phú ({count} kỹ năng), bao phủ đa dạng nhóm công nghệ và công cụ"
        elif score >= 12.0:
            return f"Đã có các kỹ năng nền tảng ({count} kỹ năng), nên bổ sung thêm công cụ thực chiến và kỹ năng mềm"
        return f"Danh sách kỹ năng còn ít ({count} kỹ năng), chưa thể hiện rõ năng lực chuyên môn"

    @staticmethod
    def _default_exp_reason(score: float, data: Dict[str, Any]) -> str:
        years = data.get("yearsExperience", 0.0)
        if score >= 18.0:
            return f"Kinh nghiệm làm việc thực tế vững chắc (~{years} năm), có mốc thời gian rõ ràng và mô tả nhiệm vụ chi tiết"
        elif score >= 12.0:
            return f"Có kinh nghiệm làm việc (~{years} năm) nhưng nên mô tả sâu hơn về vai trò và trách nhiệm từng công việc"
        return "Kinh nghiệm làm việc còn ít hoặc chưa có mô tả chi tiết quá trình công tác"

    @staticmethod
    def _default_proj_reason(score: float, data: Dict[str, Any]) -> str:
        metrics = data.get("metricsCount", 0)
        if score >= 18.0:
            return f"Dự án thực tế nổi bật, nêu rõ công nghệ và có số liệu định lượng kết quả thuyết phục ({metrics} chỉ số)"
        elif score >= 12.0:
            return "Có mô tả dự án và công nghệ nhưng còn thiếu số liệu định lượng thành tích (%, số người dùng, hiệu năng)"
        return "Chưa có mục dự án chuyên môn rõ ràng hoặc chưa nêu rõ vai trò trong dự án"

    @staticmethod
    def _default_edu_reason(score: float, data: Dict[str, Any]) -> str:
        if score >= 9.0:
            uni = data.get("university")
            return f"Học vấn đầy đủ rõ ràng (trình độ Đại học/Cao đẳng, trường đào tạo{' ' + uni if uni else ''}, chuyên ngành)"
        elif score >= 6.0:
            return "Có thông tin học vấn nhưng chưa nêu đầy đủ chuyên ngành hoặc năm tốt nghiệp"
        return "Thông tin học vấn chưa được định danh rõ ràng"

    @staticmethod
    def _default_cert_reason(score: float, data: Dict[str, Any]) -> str:
        if score >= 4.0:
            return "Có chứng chỉ chuyên môn / ngoại ngữ uy tín hoặc thành tích nổi bật"
        elif score >= 2.0:
            return "Có chứng nhận hoặc giải thưởng khuyến khích"
        return "Chưa có chứng chỉ nghề nghiệp hoặc giải thưởng (điểm khuyến khích)"

    @staticmethod
    def _default_format_reason(score: float, data: Dict[str, Any]) -> str:
        if score >= 4.0:
            return "Cấu trúc CV đầy đủ các phần cốt lõi, độ dài tiêu chuẩn và phân mục rõ ràng"
        elif score >= 2.5:
            return "Bố cục tương đối ổn nhưng độ dài hơi ngắn hoặc thiếu một số phân mục phụ"
        return "Cấu trúc CV chưa hoàn thiện hoặc nội dung quá ngắn"
