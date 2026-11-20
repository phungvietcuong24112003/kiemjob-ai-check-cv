from app.services.experience_analyzer import ExperienceAnalyzer


def test_experience_date_ranges():
    text = """
    Lập trình viên Backend
    Công ty Cổ phần Công nghệ XYZ (03/2021 - 08/2023)
    Phát triển các module microservices.
    
    Kỹ sư phần mềm
    Công ty TNHH Giải pháp ABC (09/2023 - Hiện tại)
    Phụ trách thiết kế database và tối ưu API.
    """
    res = ExperienceAnalyzer.analyze(text)
    assert res["yearsExperience"] >= 2.0
    assert "Lập Trình Viên" in res["jobTitles"] or "Kỹ Sư" in res["jobTitles"]
    assert res["score"] >= 10.0
