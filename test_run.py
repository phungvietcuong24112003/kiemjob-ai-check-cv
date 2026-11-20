"""
Script chạy thử nghiệm nhanh AI Service Check CV
Chạy lệnh: .\venv\Scripts\python test_run.py
"""

import json
from app.routes.cv_routes import analyze_cv
from app.schemas.cv_schema import CvAnalyzeRequest

# 1. Mẫu CV 1: Đầy đủ thông tin (Kỹ sư Backend Java)
CV_SAMPLE_FULL = """
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
"""

# 2. Mẫu CV 2: Thiếu thông tin (Thiếu SĐT, thiếu dự án, thiếu mục tiêu, ít kỹ năng)
CV_SAMPLE_SPARSE = """
Trần Thị Mai
Email: mai.tran@gmail.com

HỌC VẤN
Đại học Kinh tế Quốc dân (2019 - 2023)
Chuyên ngành Kế toán doanh nghiệp

KỸ NĂNG
Kế toán thuế, Excel, MISA

KINH NGHIỆM LÀM VIỆC
Công ty TNHH May mặc (2023 - 2024)
Làm hóa đơn, chứng từ sổ sách hàng ngày và hỗ trợ lập báo cáo thuế cuối năm.
"""


def print_result(title: str, response):
    print("=" * 80)
    print(f"🔥 {title}")
    print("=" * 80)
    print(f"⭐ ĐIỂM CHẤT LƯỢNG CV: {response.qualityScore} / 100")
    print("-" * 80)
    
    scoring = response.parsedData.scoring
    print("📊 BẢNG ĐIỂM CHI TIẾT 8 TIÊU CHÍ:")
    print(f"  1. Thông tin cá nhân & liên hệ : {scoring.personalInfoScore:4.1f} / 10.0")
    print(f"  2. Mục tiêu nghề nghiệp        : {scoring.objectiveScore:4.1f} / 10.0")
    print(f"  3. Kỹ năng chuyên môn          : {scoring.skillScore:4.1f} / 20.0")
    print(f"  4. Kinh nghiệm làm việc        : {scoring.experienceScore:4.1f} / 20.0")
    print(f"  5. Dự án thực tế               : {scoring.projectScore:4.1f} / 20.0")
    print(f"  6. Học vấn                     : {scoring.educationScore:4.1f} / 10.0")
    print(f"  7. Chứng chỉ & Thành tích      : {scoring.certificateScore:4.1f} /  5.0")
    print(f"  8. Cấu trúc & Định dạng        : {scoring.formatScore:4.1f} /  5.0")
    print("-" * 80)

    print("📝 TÓM TẮT HỒ SƠ ỨNG VIÊN:")
    print(f"  {response.summary}")
    print("-" * 80)

    print("💡 CÁC GỢI Ý CẢI THIỆN CV:")
    if response.suggestions:
        for idx, sug in enumerate(response.suggestions, 1):
            print(f"  {idx}. {sug}")
    else:
        print("  Hồ sơ rất hoàn thiện, không có gợi ý cải thiện bổ sung.")
    
    print("-" * 80)
    profile = response.parsedData.searchProfile
    print(f"🔍 PROFILE TÌM KIẾM ĐÃ TRÍCH XUẤT:")
    print(f"  - Ngành nghề      : {profile.industry}")
    print(f"  - Cấp bậc         : {profile.seniority}")
    print(f"  - Số năm kinh nghiệm: {profile.yearsExperience} năm")
    print(f"  - Kỹ năng nhận diện ({len(profile.skills)}): {', '.join(profile.skills)}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print("\n🚀 BẮT ĐẦU CHẠY KIỂM THỬ AI SERVICE CHECK CV...\n")
    
    # Test CV 1
    res1 = analyze_cv(CvAnalyzeRequest(text=CV_SAMPLE_FULL))
    print_result("KẾT QUẢ PHÂN TÍCH CV 1: ĐẦY ĐỦ THÔNG TIN (BACKEND JAVA)", res1)

    # Test CV 2
    res2 = analyze_cv(CvAnalyzeRequest(text=CV_SAMPLE_SPARSE))
    print_result("KẾT QUẢ PHÂN TÍCH CV 2: THIẾU THÔNG TIN (KẾ TOÁN)", res2)
