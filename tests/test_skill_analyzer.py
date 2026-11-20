from app.services.skill_analyzer import SkillAnalyzer


def test_extract_skills_vietnamese_text():
    text = """
    Ứng viên thành thạo ngôn ngữ Java và framework Spring Boot.
    Đã từng triển khai hệ thống với Docker, Kubernetes (k8s) và cơ sở dữ liệu PostgreSQL.
    Có kinh nghiệm làm việc với Redis và CI/CD (GitLab CI).
    """
    res = SkillAnalyzer.analyze(text)
    skills = res["skills"]
    assert "java" in skills
    assert "spring boot" in skills
    assert "docker" in skills
    assert "postgresql" in skills
    assert "kubernetes" in skills  # K8s synonym mapped
    assert res["score"] >= 10.0


def test_extract_accounting_skills():
    text = "Kế toán tổng hợp 3 năm kinh nghiệm, thành thạo phần mềm MISA, báo cáo tài chính và kê khai thuế."
    res = SkillAnalyzer.analyze(text)
    skills = res["skills"]
    assert "kế toán tổng hợp" in skills
    assert "misa" in skills
    assert "báo cáo tài chính" in skills
