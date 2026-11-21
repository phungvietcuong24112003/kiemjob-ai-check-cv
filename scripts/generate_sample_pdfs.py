"""
Script tự động sinh 8 file PDF CV mẫu phục vụ kiểm thử cho KiemJob AI Service.
Chạy: .\venv\Scripts\python scripts/generate_sample_pdfs.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Đăng ký font hỗ trợ tiếng Việt
FONT_NAME = "Helvetica"
if os.path.exists("C:\\Windows\\Fonts\\arial.ttf"):
    try:
        pdfmetrics.registerFont(TTFont("ArialVN", "C:\\Windows\\Fonts\\arial.ttf"))
        FONT_NAME = "ArialVN"
    except Exception:
        FONT_NAME = "Helvetica"


def create_pdf(filepath: str, text: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont(FONT_NAME, 10)
    for line in text.strip().splitlines():
        line_str = line.strip()
        if not line_str:
            y -= 12
            continue
        if y < 50:
            c.showPage()
            c.setFont(FONT_NAME, 10)
            y = height - 50
        c.drawString(50, y, line_str)
        y -= 15

    c.save()
    print(f"✅ Đã tạo: {filepath}")


SAMPLES = {
    # 1. CV tốt, đầy đủ thông tin (Backend Java)
    "cv_1_good_full.pdf": """
NGUYỄN VĂN AN
Email: an.nguyen@gmail.com - SĐT: 0987654321
LinkedIn: https://linkedin.com/in/annguyen - GitHub: https://github.com/annguyen
Địa chỉ: Cầu Giấy, Hà Nội

MỤC TIÊU NGHỀ NGHIỆP
Mong muốn phát triển chuyên môn trở thành Kỹ sư phần mềm cao cấp (Senior Backend Engineer) trong 2 năm tới, cống hiến giải pháp tối ưu hiệu năng hệ thống cho doanh nghiệp.

HỌC VẤN
Đại học Bách Khoa Hà Nội (2018 - 2022)
Chuyên ngành: Công nghệ thông tin - Tốt nghiệp loại Giỏi

KỸ NĂNG CHUYÊN MÔN
- Ngôn ngữ: Java, Python, SQL, JavaScript
- Framework & Thư viện: Spring Boot, Spring Security, Hibernate, FastAPI, React
- Cơ sở dữ liệu: PostgreSQL, MySQL, Redis, MongoDB
- DevOps & Cloud: Docker, Kubernetes, AWS, CI/CD, Git, Linux
- Kỹ năng mềm: Làm việc nhóm, tư duy giải quyết vấn đề, quản lý thời gian

KINH NGHIỆM LÀM VIỆC
Công ty Cổ phần Công nghệ ABC (06/2022 - Hiện tại)
Vị trí: Lập trình viên Backend Java
- Thiết kế và phát triển hệ thống thanh toán và đơn hàng phục vụ hơn 80.000 người dùng hoạt động hàng ngày.
- Tối ưu hóa truy vấn cơ sở dữ liệu PostgreSQL giúp giảm 40% thời gian phản hồi API.
- Viết unit test đạt độ bao phủ kiểm thử (coverage) trên 85%.

DỰ ÁN NỔI BẬT
Hệ thống Thương Mại Điện Tử Đa Nền Tảng
- Vai trò: Trưởng nhóm kỹ thuật Backend (5 thành viên)
- Công nghệ: Java 17, Spring Boot, Kafka, Docker, Redis, PostgreSQL
- Kết quả: Xử lý 1.200 requests/s và giảm tỷ lệ lỗi xuống dưới 0.05%.

CHỨNG CHỈ & THÀNH TÍCH
- Chứng chỉ AWS Certified Solutions Architect Associate (2023)
- Chứng chỉ ngoại ngữ TOEIC 820
- Giải Ba Olympic Tin học sinh viên (2021)
""",

    # 2. CV thiếu thông tin cá nhân (thiếu SĐT, thiếu link)
    "cv_2_missing_contact.pdf": """
LÊ HOÀNG NAM
Email: nam.le@gmail.com

MỤC TIÊU NGHỀ NGHIỆP
Tìm kiếm cơ hội việc làm vị trí Frontend Developer để vận dụng kiến thức ReactJS và TypeScript.

HỌC VẤN
Đại học Công nghệ - ĐHQGHN (2019 - 2023)
Ngành Khoa học Máy tính

KỸ NĂNG
React, TypeScript, HTML, CSS, JavaScript, Tailwind, Git

KINH NGHIỆM LÀM VIỆC
Công ty Phần mềm XYZ (2023 - 2024)
Lập trình viên Frontend
Phát triển giao diện người dùng theo thiết kế Figma và kết nối REST API.

DỰ ÁN
Website Quản lý Nhân sự
Công nghệ: React, Redux Toolkit, Tailwind CSS
Xây dựng các màn hình quản lý bảng chấm công và tính lương.
""",

    # 3. CV chỉ có học vấn, chưa có kinh nghiệm (Fresher)
    "cv_3_fresher_education_only.pdf": """
PHẠM MINH ĐỨC
Email: duc.pham@gmail.com - SĐT: 0912345678
Địa chỉ: Đà Nẵng

MỤC TIÊU NGHỀ NGHIỆP
Sinh viên mới tốt nghiệp mong muốn tìm kiếm vị trí Thực tập sinh hoặc Fresher Java Developer để học hỏi và rèn luyện kinh nghiệm thực chiến.

HỌC VẤN
Đại học Bách Khoa - Đại học Đà Nẵng (2020 - 2024)
Chuyên ngành: Kỹ thuật Phần mềm - GPA: 3.2/4.0

KỸ NĂNG
Java cơ bản, OOP, SQL, Git, HTML, CSS, Spring Boot

HOẠT ĐỘNG
Thành viên Câu lạc bộ Tin học trường Đại học Bách Khoa (2021 - 2023)
Tham gia tổ chức các buổi hội thảo công nghệ cho sinh viên.
""",

    # 4. CV có nhiều dự án và số liệu thực tế
    "cv_4_many_projects.pdf": """
VŨ ĐÌNH TRỌNG
Email: trong.vu@example.com - SĐT: 0933445566
LinkedIn: https://linkedin.com/in/trongvu
Địa chỉ: TP.HCM

MỤC TIÊU NGHỀ NGHIỆP
Kỹ sư Giải pháp Đám mây (Cloud & DevOps Engineer) với mong muốn tối ưu hóa hạ tầng và tự động hóa quy trình CI/CD cho các hệ thống quy mô lớn.

KỸ NĂNG CHUYÊN MÔN
AWS, Docker, Kubernetes, Terraform, Ansible, Jenkins, Python, Bash, Prometheus, Grafana

KINH NGHIỆM & DỰ ÁN NỔI BẬT
1. Dự án Di chuyển Hạ tầng Lên AWS (AWS Cloud Migration)
- Vai trò: Kỹ sư DevOps chính
- Công nghệ: AWS EKS, Terraform, Helm, GitHub Actions
- Kết quả: Tiết kiệm 30% chi phí vận hành hàng tháng (hơn 15.000 USD/tháng) và giảm thời gian triển khai 70%.

2. Hệ thống Giám sát Tập trung (Monitoring System)
- Vai trò: Thiết kế và triển khai
- Công nghệ: Prometheus, Grafana, Loki, Alertmanager
- Kết quả: Theo dõi hơn 200 microservices phục vụ 500.000 users, giảm thời gian phát hiện sự cố (MTTD) từ 45 phút xuống dưới 3 phút.

3. Nền tảng CI/CD Tự động hóa
- Công nghệ: GitLab CI, SonarQube, ArgoCD
- Kết quả: Đạt tần suất triển khai 15 lần/ngày với tỷ lệ thành công 99.8%.

CHỨNG CHỈ
- AWS Certified DevOps Engineer Professional (2023)
- Certified Kubernetes Administrator (CKA - 2022)
""",

    # 5. CV tiếng Anh
    "cv_5_english.pdf": """
DAVID NGUYEN
Email: david.nguyen@email.com | Phone: +84977112233
LinkedIn: https://linkedin.com/in/davidnguyen | GitHub: https://github.com/davidnguyen
Location: Ho Chi Minh City, Vietnam

PROFESSIONAL SUMMARY
Senior Full-stack Software Engineer with 5 years of experience architecting and delivering high-traffic web platforms using React, Node.js, and AWS. Proven track record in leading engineering teams and optimizing distributed systems.

EDUCATION
Ho Chi Minh City University of Technology (2016 - 2020)
Bachelor of Science in Computer Science - GPA: 3.6/4.0

TECHNICAL SKILLS
- Languages: JavaScript, TypeScript, Python, Golang, SQL
- Frontend: React, Next.js, Redux, Tailwind CSS
- Backend: Node.js, Express, NestJS, PostgreSQL, Redis, RabbitMQ
- Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, CI/CD, Git

WORK EXPERIENCE
Lead Software Engineer - Global Solutions Inc. (03/2022 - Present)
- Led a team of 6 engineers to build scalable fintech platforms serving 250,000 active users.
- Reduced database latency by 45% through Redis caching and query indexing in PostgreSQL.
- Implemented automated CI/CD pipelines achieving 99.95% system uptime.

Full-stack Developer - FinTech Asia (06/2020 - 02/2022)
- Built interactive customer dashboards with Next.js and Tailwind CSS.
- Developed RESTful APIs processing over 1,500 transactions per second.

CERTIFICATIONS
- AWS Certified Solutions Architect Associate (2022)
- Professional Scrum Master (PSM I - 2021)
""",

    # 6. CV tiếng Việt (Kế toán)
    "cv_6_vietnamese.pdf": """
NGUYỄN THỊ THU HÀ
Email: thuha.ketoan@gmail.com - SĐT: 0978123456
Địa chỉ: Đống Đa, Hà Nội

MỤC TIÊU NGHỀ NGHIỆP
Kế toán tổng hợp với 3 năm kinh nghiệm mong muốn tìm kiếm môi trường làm việc chuyên nghiệp để phát huy năng lực kiểm soát chi phí và tối ưu hóa quy trình tài chính doanh nghiệp.

HỌC VẤN
Học viện Tài chính (2017 - 2021)
Chuyên ngành: Kế toán - Kiểm toán - Xếp loại: Giỏi

KỸ NĂNG CHUYÊN MÔN
- Kế toán tổng hợp, kế toán thuế, lập báo cáo tài chính
- Thành thạo phần mềm kế toán MISA, FAST, BRAVO, Excel nâng cao
- Kê khai thuế qua mạng, hóa đơn điện tử, quyết toán thuế TNDN và TNCN
- Kỹ năng phân tích dòng tiền và kiểm soát ngân sách

KINH NGHIỆM LÀM VIỆC
Công ty Cổ phần Thương mại Minh Phát (07/2021 - Hiện tại)
Vị trí: Kế toán tổng hợp
- Lập báo cáo tài chính quý, năm và kê khai thuế định kỳ đầy đủ, chính xác.
- Theo dõi và đối chiếu công nợ khách hàng trị giá hơn 20 tỷ đồng/tháng.
- Đề xuất quy trình số hóa hóa đơn giúp giảm 50% thời gian xử lý chứng từ sổ sách.

CHỨNG CHỈ
- Chứng chỉ Kế toán trưởng doanh nghiệp (Bộ Tài chính cấp - 2023)
- Chứng chỉ Tin học Văn phòng MOS Excel Expert
""",

    # 7. CV có nội dung rất ngắn
    "cv_7_short.pdf": """
Trần Văn Hùng
Email: hung@gmail.com
Học vấn: Đại học Mở
Kỹ năng: Java, SQL
Kinh nghiệm: Chưa có kinh nghiệm thực tế.
""",

    # 8. CV có nội dung không liên quan đến tuyển dụng (bài thơ / truyện)
    "cv_8_unrelated.pdf": """
BÀI THƠ MÙA THU
Tác giả: Khuyết danh

Gió mùa thu xào xạc lá vàng rơi
Mây trắng lững lờ trôi cuối chân trời
Dòng sông êm đềm trôi về biển lớn
Thuyền ai xa bến vắng một chiều đông.

Thiên nhiên tươi đẹp và thanh bình biết bao.
Cảnh sắc đất trời khiến lòng người cảm thấy thư thái.
Hôm nay là một ngày tuyệt vời để đi dạo trong công viên.
"""
}


def main():
    target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_cvs")
    print(f"Bắt đầu tạo các file PDF mẫu tại: {target_dir}")
    for filename, content in SAMPLES.items():
        filepath = os.path.join(target_dir, filename)
        create_pdf(filepath, content)
    print("\n🎉 Đã tạo xong tất cả 8 file PDF CV mẫu thành công!")


if __name__ == "__main__":
    main()
