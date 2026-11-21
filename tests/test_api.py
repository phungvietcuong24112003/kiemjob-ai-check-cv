from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "UP"
    assert data["service"] == "ai-service-check-cv"


def test_analyze_full_cv():
    cv_sample = """
    NGUYỄN VĂN AN
    Email: an.nguyen@example.com - SĐT: 0987654321
    LinkedIn: https://linkedin.com/in/annguyen - GitHub: https://github.com/annguyen
    Địa chỉ: Cầu Giấy, Hà Nội

    MỤC TIÊU NGHỀ NGHIỆP
    Mong muốn trở thành Kỹ sư phần mềm xuất sắc trong 2 năm tới, cống hiến giá trị giải pháp tối ưu cho doanh nghiệp và nâng cao chuyên môn.

    HỌC VẤN
    Đại học Bách Khoa Hà Nội (2018 - 2022)
    Chuyên ngành: Công nghệ thông tin - GPA: 3.4/4.0

    KỸ NĂNG CHUYÊN MÔN
    - Ngôn ngữ & Framework: Java, Spring Boot, Python, FastAPI, React
    - Cơ sở dữ liệu: PostgreSQL, MySQL, Redis
    - DevOps & Tools: Docker, Git, CI/CD, Linux

    KINH NGHIỆM LÀM VIỆC
    Công ty Cổ phần Công nghệ ABC (06/2022 - Hiện tại)
    Vị trí: Lập trình viên Backend
    - Thiết kế và phát triển RESTful API cho nền tảng e-commerce phục vụ 100.000 users.
    - Tối ưu hóa câu truy vấn cơ sở dữ liệu giúp giảm 35% thời gian phản hồi hệ thống.
    - Phối hợp nhóm Agile Scrum gồm 8 thành viên.

    DỰ ÁN NỔI BẬT
    Hệ thống Quản lý Bán hàng Đa kênh
    - Vai trò: Trưởng nhóm kỹ thuật
    - Công nghệ sử dụng: Java 17, Spring Boot, Kafka, Docker, PostgreSQL
    - Kết quả: Xử lý hơn 500 requests/s và giảm tỷ lệ lỗi hệ thống xuống dưới 0.1%.

    CHỨNG CHỈ & THÀNH TÍCH
    - Chứng chỉ AWS Certified Solutions Architect Associate (2023)
    - Chứng chỉ tiếng Anh TOEIC 850
    """

    res = client.post(
        "/api/v1/analyze-cv",
        json={"text": cv_sample}
    )

    assert res.status_code == 200
    data = res.json()
    assert "qualityScore" in data
    assert data["qualityScore"] >= 75.0
    assert "suggestions" in data
    assert "summary" in data
    assert "scoring" in data

    scoring = data["scoring"]
    assert scoring["personalInfo"]["score"] == 10.0
    assert scoring["skills"]["score"] >= 15.0
    assert scoring["projects"]["score"] >= 15.0

    personal = data["personalInfo"]
    assert personal["email"] == "an.nguyen@example.com"
    assert personal["phone"] == "0987654321"

    skills = data["skills"]
    assert "java" in [s.lower() for s in skills]
    assert "spring boot" in [s.lower() for s in skills]
