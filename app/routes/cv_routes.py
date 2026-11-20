from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_internal_secret
from app.core.config import settings
from app.schemas.cv_schema import (
    CvAnalyzeRequest,
    CvAnalyzeResponse,
    ParsedCvData,
    ScoringBreakdown,
    PersonalInfo,
    SearchProfile,
)
from app.services import (
    TextCleaner,
    PersonalInfoAnalyzer,
    ObjectiveAnalyzer,
    SkillAnalyzer,
    ExperienceAnalyzer,
    ProjectAnalyzer,
    EducationAnalyzer,
    CertificateAnalyzer,
    FormatAnalyzer,
    ScoreCalculator,
    SuggestionGenerator,
    SummaryGenerator,
)

router = APIRouter(prefix="/api/v1/cv", tags=["CV Analysis"])


@router.post("/analyze", response_model=CvAnalyzeResponse, dependencies=[Depends(verify_internal_secret)])
def analyze_cv(request: CvAnalyzeRequest):
    raw_text = request.text
    if not raw_text or len(raw_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Văn bản CV quá ngắn hoặc không có nội dung")

    # 1. Làm sạch văn bản và phân tách các phần
    cleaned_text = TextCleaner.clean(raw_text)
    sections = TextCleaner.split_sections(cleaned_text)

    # 2. Phân tích 8 nhóm tiêu chí
    personal_info_res = PersonalInfoAnalyzer.analyze(cleaned_text, sections.get("header", ""))
    objective_res = ObjectiveAnalyzer.analyze(cleaned_text, sections.get("objective", ""))
    skill_res = SkillAnalyzer.analyze(cleaned_text, sections.get("skills", ""))
    experience_res = ExperienceAnalyzer.analyze(cleaned_text, sections.get("experience", ""))
    project_res = ProjectAnalyzer.analyze(cleaned_text, sections.get("projects", ""))
    education_res = EducationAnalyzer.analyze(cleaned_text, sections.get("education", ""))
    certificate_res = CertificateAnalyzer.analyze(cleaned_text, sections.get("certificates", ""))
    format_res = FormatAnalyzer.analyze(cleaned_text, sections)

    # 3. Tính điểm tổng và bảng điểm chi tiết
    score_res = ScoreCalculator.calculate_total(
        personal_info=personal_info_res,
        objective=objective_res,
        skills=skill_res,
        experience=experience_res,
        projects=project_res,
        education=education_res,
        certificates=certificate_res,
        format_info=format_res,
    )

    # 4. Sinh gợi ý cải thiện và tóm tắt CV
    suggestions = SuggestionGenerator.generate(
        personal_info=personal_info_res,
        objective=objective_res,
        skills=skill_res,
        experience=experience_res,
        projects=project_res,
        education=education_res,
        certificates=certificate_res,
        format_info=format_res,
    )

    summary = SummaryGenerator.generate(
        personal_info=personal_info_res,
        experience=experience_res,
        skills=skill_res,
        education=education_res,
        projects=project_res,
    )

    # 5. Xác định nhóm ngành phù hợp
    industry = "Công nghệ thông tin"
    categories = skill_res.get("categories", [])
    if "accounting_finance" in categories:
        industry = "Kế toán / Kiểm toán"
    elif "marketing_sales" in categories:
        industry = "Marketing / Truyền thông"

    # 6. Chuẩn bị DTO phản hồi
    scoring_dto = ScoringBreakdown(**score_res["scoring"])
    personal_info_dto = PersonalInfo(
        fullName=personal_info_res.get("fullName"),
        email=personal_info_res.get("email"),
        phone=personal_info_res.get("phone"),
        location=personal_info_res.get("location"),
        links=personal_info_res.get("links", []),
    )
    search_profile_dto = SearchProfile(
        jobTitles=experience_res.get("jobTitles", []),
        skills=skill_res.get("skills", []),
        yearsExperience=experience_res.get("yearsExperience", 0.0),
        seniority=experience_res.get("seniority", "unknown"),
        educationLevel=education_res.get("educationLevel", "dai_hoc"),
        industry=industry,
    )

    parsed_data = ParsedCvData(
        scoring=scoring_dto,
        personalInfo=personal_info_dto,
        searchProfile=search_profile_dto,
        details={
            "metrics": project_res.get("metricsFound", []),
            "certificates": certificate_res.get("certificates", []),
            "awards": certificate_res.get("awards", []),
            "university": education_res.get("university"),
            "wordCount": format_res.get("wordCount", 0),
        },
    )

    return CvAnalyzeResponse(
        qualityScore=score_res["qualityScore"],
        summary=summary,
        suggestions=suggestions,
        parsedData=parsed_data,
        algorithmVersion=settings.ALGORITHM_VERSION,
    )
