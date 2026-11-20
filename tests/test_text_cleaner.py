from app.services.text_cleaner import TextCleaner


def test_clean_text_normalizes_bullets_and_spaces():
    raw = "Nguyễn Văn A\u2022 Lập trình viên   \n\n\n\nKỹ năng: Java,   Spring\uF0B7"
    cleaned = TextCleaner.clean(raw)
    assert "•" not in cleaned
    assert "\uF0B7" not in cleaned
    assert " - Lập trình viên" in cleaned
    assert "\n\n\n\n" not in cleaned


def test_split_sections():
    cv = """
NGUYỄN VĂN A
Email: a@gmail.com

MỤC TIÊU NGHỀ NGHIỆP
Phát triển thành Senior Java Developer trong 2 năm tới.

KINH NGHIỆM LÀM VIỆC
Công ty ABC (01/2022 - Hiện tại)
Lập trình viên Backend

KỸ NĂNG CHUYÊN MÔN
Java, Spring Boot, PostgreSQL, Docker

HỌC VẤN
Đại học Bách Khoa Hà Nội
    """
    sections = TextCleaner.split_sections(cv)
    assert "objective" in sections
    assert "experience" in sections
    assert "skills" in sections
    assert "education" in sections
    assert "Senior Java Developer" in sections["objective"]
    assert "Spring Boot" in sections["skills"]
