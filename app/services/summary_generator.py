from typing import Dict, Any


class SummaryGenerator:
    @classmethod
    def generate(
        cls,
        personal_info: Dict[str, Any],
        experience: Dict[str, Any],
        skills: Dict[str, Any],
        education: Dict[str, Any],
        projects: Dict[str, Any]
    ) -> str:
        """
        Sinh bản tóm tắt hồ sơ chuyên nghiệp, súc tích (3-4 câu).
        """
        name = personal_info.get("fullName") or "Ứng viên"
        years = experience.get("yearsExperience", 0.0)
        seniority = experience.get("seniority", "mid-level")
        job_titles = experience.get("jobTitles", [])
        primary_title = job_titles[0] if job_titles else "Chuyên viên"

        skill_list = skills.get("skills", [])
        top_skills = ", ".join(skill_list[:5]) if skill_list else "các kỹ năng chuyên môn cốt lõi"

        edu_level = education.get("educationLevel", "dai_hoc")
        edu_str = "trình độ Đại học" if edu_level == "dai_hoc" else ("trình độ Thạc sĩ" if edu_level == "thac_si" else "trình độ chuyên môn")
        if education.get("university"):
            edu_str += f" ({education.get('university')})"

        # Xây dựng câu tóm tắt
        parts = []

        if years >= 1.0:
            parts.append(f"{name} là {primary_title} với khoảng {years} năm kinh nghiệm thực tế.")
        elif years > 0:
            parts.append(f"{name} là {primary_title} tiềm năng với kinh nghiệm thực tập và dự án thực tế.")
        else:
            parts.append(f"{name} có định hướng nghề nghiệp rõ ràng ở vị trí {primary_title}.")

        if skill_list:
            parts.append(f"Có năng lực chuyên môn tập trung vào: {top_skills}.")

        metrics = projects.get("metricsFound", [])
        if metrics:
            parts.append(f"Hồ sơ nổi bật với các thành tích và dự án đã định lượng kết quả.")
        
        parts.append(f"Học vấn đạt {edu_str}.")

        return " ".join(parts)
