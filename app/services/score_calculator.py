from typing import Dict, Any


class ScoreCalculator:
    MAX_SCORES = {
        "personal_info": 10.0,
        "objective": 10.0,
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
        Tính điểm tổng và chuẩn hóa điểm từng phần theo thang điểm 100.
        """
        p_score = min(float(personal_info.get("score", 0.0)), cls.MAX_SCORES["personal_info"])
        o_score = min(float(objective.get("score", 0.0)), cls.MAX_SCORES["objective"])
        s_score = min(float(skills.get("score", 0.0)), cls.MAX_SCORES["skills"])
        e_score = min(float(experience.get("score", 0.0)), cls.MAX_SCORES["experience"])
        proj_score = min(float(projects.get("score", 0.0)), cls.MAX_SCORES["projects"])
        edu_score = min(float(education.get("score", 0.0)), cls.MAX_SCORES["education"])
        cert_score = min(float(certificates.get("score", 0.0)), cls.MAX_SCORES["certificates"])
        f_score = min(float(format_info.get("score", 0.0)), cls.MAX_SCORES["format"])

        total = p_score + o_score + s_score + e_score + proj_score + edu_score + cert_score + f_score
        total = round(min(max(total, 0.0), 100.0), 1)

        breakdown = {
            "personalInfoScore": round(p_score, 1),
            "objectiveScore": round(o_score, 1),
            "skillScore": round(s_score, 1),
            "experienceScore": round(e_score, 1),
            "projectScore": round(proj_score, 1),
            "educationScore": round(edu_score, 1),
            "certificateScore": round(cert_score, 1),
            "formatScore": round(f_score, 1)
        }

        return {
            "qualityScore": total,
            "scoring": breakdown
        }
