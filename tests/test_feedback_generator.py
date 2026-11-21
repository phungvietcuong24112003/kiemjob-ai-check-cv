import pytest
from app.services.feedback_generator import FeedbackGenerator
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_good_cv_feedback():
    personal = {
        "fullName": "Nguyễn Văn A",
        "phone": "0987654321",
        "email": "nguyenvana@gmail.com",
        "location": "Hà Nội",
        "links": ["https://linkedin.com/in/nguyenvana", "https://github.com/nguyenvana"],
        "score": 10.0
    }
    objective = {
        "wordCount": 35,
        "score": 9.0
    }
    skills = {
        "skills": ["Java", "Spring Boot", "Docker", "PostgreSQL", "Redis", "Kafka", "Git"],
        "categories": ["backend", "database", "devops"],
        "score": 20.0
    }
    experience = {
        "hasExperience": True,
        "yearsExperience": 3.0,
        "score": 18.0
    }
    projects = {
        "details": {"hasProjects": True},
        "metricsFound": ["30% tối ưu tốc độ", "10.000 người dùng"],
        "metricsCount": 2,
        "score": 19.0
    }
    education = {
        "university": "Đại học Bách Khoa Hà Nội",
        "educationLevel": "dai_hoc",
        "score": 10.0
    }
    certificates = {
        "certificates": ["AWS Certified Solutions Architect", "TOEIC 850"],
        "score": 5.0
    }
    format_info = {
        "wordCount": 650,
        "sectionsCount": 7,
        "score": 5.0
    }

    feedback = FeedbackGenerator.generate(
        personal_info=personal,
        objective=objective,
        skills=skills,
        experience=experience,
        projects=projects,
        education=education,
        certificates=certificates,
        format_info=format_info,
        quality_score=92.0,
        language="vi"
    )

    assert isinstance(feedback["strengths"], list)
    assert isinstance(feedback["weaknesses"], list)
    assert isinstance(feedback["suggestions"], list)
    assert len(feedback["strengths"]) >= 4
    assert len(feedback["weaknesses"]) <= 1
    # Check that personal info is praised as strength
    assert any("liên hệ" in s.lower() for s in feedback["strengths"])


def test_poor_cv_feedback():
    personal = {
        "fullName": "Nguyễn Văn B",
        "phone": None,
        "email": None,
        "location": None,
        "links": [],
        "score": 2.0
    }
    objective = {
        "wordCount": 5,
        "score": 2.0
    }
    skills = {
        "skills": ["Python"],
        "categories": [],
        "score": 4.0
    }
    experience = {
        "hasExperience": False,
        "yearsExperience": 0.0,
        "score": 0.0
    }
    projects = {
        "details": {"hasProjects": False},
        "metricsFound": [],
        "metricsCount": 0,
        "score": 0.0
    }
    education = {
        "university": None,
        "educationLevel": "dai_hoc",
        "score": 4.0
    }
    certificates = {
        "certificates": [],
        "score": 0.0
    }
    format_info = {
        "wordCount": 120,
        "sectionsCount": 2,
        "score": 1.0
    }

    feedback = FeedbackGenerator.generate(
        personal_info=personal,
        objective=objective,
        skills=skills,
        experience=experience,
        projects=projects,
        education=education,
        certificates=certificates,
        format_info=format_info,
        quality_score=25.0,
        language="vi"
    )

    assert len(feedback["weaknesses"]) >= 4
    assert len(feedback["suggestions"]) >= 4
    # Check that contact info weakness is detected
    assert any("liên hệ" in w.lower() for w in feedback["weaknesses"])


def test_english_cv_feedback():
    personal = {
        "fullName": "John Doe",
        "phone": "+1 234 567 890",
        "email": "johndoe@gmail.com",
        "location": "New York, USA",
        "links": ["https://linkedin.com/in/johndoe"],
        "score": 10.0
    }
    objective = {
        "wordCount": 40,
        "score": 10.0
    }
    skills = {
        "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "AWS"],
        "categories": ["backend", "frontend", "devops"],
        "score": 20.0
    }
    experience = {
        "hasExperience": True,
        "yearsExperience": 2.5,
        "score": 18.0
    }
    projects = {
        "details": {"hasProjects": True},
        "metricsFound": ["40% latency reduction"],
        "metricsCount": 1,
        "score": 19.0
    }
    education = {
        "university": "MIT",
        "educationLevel": "dai_hoc",
        "score": 10.0
    }
    certificates = {
        "certificates": ["AWS Developer Associate"],
        "score": 5.0
    }
    format_info = {
        "wordCount": 500,
        "sectionsCount": 6,
        "score": 5.0
    }

    feedback = FeedbackGenerator.generate(
        personal_info=personal,
        objective=objective,
        skills=skills,
        experience=experience,
        projects=projects,
        education=education,
        certificates=certificates,
        format_info=format_info,
        quality_score=90.0,
        language="en"
    )

    # Should be in English
    assert any("contact" in s.lower() for s in feedback["strengths"])
    assert any("skill" in s.lower() for s in feedback["strengths"])


def test_api_analyze_with_strengths_and_weaknesses():
    sample_cv = """
    NGUYỄN VĂN AN
    Email: an.nguyen@gmail.com | SĐT: 0912345678 | GitHub: github.com/annguyen
    MỤC TIÊU NGHỀ NGHIỆP
    Lập trình viên Java Backend với định hướng phát triển hệ thống phân tán hiệu năng cao, mong muốn đóng góp vào các dự án lớn tại doanh nghiệp.
    KỸ NĂNG CHUYÊN MÔN
    - Ngôn ngữ: Java, SQL, Python
    - Frameworks: Spring Boot, Hibernate, FastAPI
    - Cơ sở dữ liệu: PostgreSQL, Redis, MySQL
    - Công cụ: Docker, Git, CI/CD, Kafka
    KINH NGHIỆM LÀM VIỆC
    Công ty Cổ phần Công nghệ ABC (06/2022 - Hiện tại)
    Vị trí: Backend Developer
    - Xây dựng RESTful API cho ứng dụng thanh toán với 10.000 giao dịch mỗi ngày.
    - Tối ưu hóa truy vấn PostgreSQL giúp cải thiện 35% thời gian phản hồi.
    HỌC VẤN
    Đại học Bách Khoa Hà Nội (2018 - 2022)
    Chuyên ngành: Công nghệ thông tin
    CHỨNG CHỈ
    - AWS Certified Cloud Practitioner
    - TOEIC 800
    """

    res = client.post("/api/v1/cv/analyze", json={"text": sample_cv})
    assert res.status_code == 200
    data = res.json()

    assert "strengths" in data
    assert "weaknesses" in data
    assert "suggestions" in data
    assert isinstance(data["strengths"], list)
    assert isinstance(data["weaknesses"], list)
    assert isinstance(data["suggestions"], list)
    assert len(data["strengths"]) > 0
    assert data["qualityScore"] > 70
