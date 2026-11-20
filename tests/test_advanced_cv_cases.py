import time
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_english_cv_analysis():
    english_cv = """
    JOHN DOE
    Email: john.doe@email.com | Phone: +84988776655
    LinkedIn: https://linkedin.com/in/johndoe | GitHub: https://github.com/johndoe
    Location: Ho Chi Minh City, Vietnam

    PROFESSIONAL SUMMARY
    Dedicated Full-stack Developer with 4 years of experience delivering robust web applications using React, Node.js, and AWS. Seeking to leverage cloud engineering expertise in a growth-oriented company.

    EDUCATION
    Ho Chi Minh City University of Technology (2017 - 2021)
    Bachelor of Computer Science - GPA: 3.5/4.0

    TECHNICAL SKILLS
    - Languages: JavaScript, TypeScript, Python, SQL
    - Frameworks: React, Express, NestJS, FastAPI, TailwindCSS
    - Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Git

    WORK EXPERIENCE
    Software Engineer - Tech Corp (07/2021 - Present)
    - Developed microservices architecture handling 50,000 requests/s with 99.9% uptime.
    - Optimized database queries in PostgreSQL, reducing latency by 40%.
    - Collaborated with cross-functional teams in an Agile Scrum environment.

    KEY PROJECTS
    Cloud Logistics Tracking Platform
    - Role: Lead Developer
    - Technologies: React, TypeScript, Node.js, Docker, AWS
    - Results: Decreased tracking dispatch delays by 25% for 12,000 active clients.

    CERTIFICATIONS & AWARDS
    - AWS Certified Solutions Architect
    - Hackathon First Prize Winner (2020)
    """

    res = client.post(
        "/api/v1/cv/analyze",
        headers={"X-Internal-Secret": settings.INTERNAL_SECRET_KEY},
        json={"text": english_cv}
    )

    assert res.status_code == 200
    data = res.json()
    assert data["qualityScore"] >= 80.0
    assert len(data["suggestions"]) > 0
    assert "react" in data["parsedData"]["searchProfile"]["skills"]
    assert data["parsedData"]["personalInfo"]["email"] == "john.doe@email.com"


def test_missing_info_cv_suggestions():
    # CV thiếu số điện thoại, thiếu dự án, thiếu mục tiêu
    sparse_cv = """
    Trần Thị Mai
    Email: mai.tran@gmail.com
    
    Học vấn:
    Đại học Kinh tế Quốc dân (2019 - 2023)
    Chuyên ngành Kế toán doanh nghiệp
    
    Kỹ năng:
    Kế toán thuế, MISA, Excel
    
    Kinh nghiệm:
    Kế toán viên tại Công ty Dệt may (2023 - 2024)
    Thực hiện hóa đơn và kiểm tra chứng từ sổ sách.
    """

    res = client.post(
        "/api/v1/cv/analyze",
        headers={"X-Internal-Secret": settings.INTERNAL_SECRET_KEY},
        json={"text": sparse_cv}
    )

    assert res.status_code == 200
    data = res.json()
    suggestions = data["suggestions"]

    # Phải có gợi ý bổ sung số điện thoại
    assert any("số điện thoại" in s.lower() for s in suggestions)
    # Phải có gợi ý về dự án hoặc số liệu hoặc mục tiêu
    assert any("mục tiêu" in s.lower() or "dự án" in s.lower() or "số liệu" in s.lower() for s in suggestions)
    # Điểm sẽ thấp hơn CV chuẩn
    assert data["qualityScore"] < 70.0


def test_cv_too_short_raises_400():
    res = client.post(
        "/api/v1/cv/analyze",
        headers={"X-Internal-Secret": settings.INTERNAL_SECRET_KEY},
        json={"text": "Quá ngắn"}
    )
    # Pydantic validation hoặc endpoint error
    assert res.status_code in [400, 422]


def test_performance_benchmark():
    sample = """
    Nguyễn Văn Test - 0912345678 - test@gmail.com
    Mục tiêu: Phát triển bản thân trong ngành công nghệ thông tin.
    Kỹ năng: Java, Spring Boot, MySQL, Docker, Git.
    Kinh nghiệm: Lập trình viên tại Công ty ABC từ 2021 đến 2024.
    Dự án: Hệ thống quản lý bán hàng với 1.000 người dùng, tối ưu 20% chi phí.
    Học vấn: Đại học Bách Khoa.
    Chứng chỉ: TOEIC 750.
    """

    start_time = time.time()
    res = client.post(
        "/api/v1/cv/analyze",
        headers={"X-Internal-Secret": settings.INTERNAL_SECRET_KEY},
        json={"text": sample}
    )
    elapsed_ms = (time.time() - start_time) * 1000

    assert res.status_code == 200
    # Phải xử lý cực nhanh dưới 200mss
    assert elapsed_ms < 200.0, f"Xử lý quá chậm: {elapsed_ms}ms"
