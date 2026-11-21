from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.utils.language_detector import LanguageDetector
from app.schemas.cv_schema import (
    AnalyzeCvRequest,
    CvAnalyzeResponse,
    PersonalInfo,
    ExperienceDetail,
    EducationDetail,
    ProjectDetail,
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
    FeedbackGenerator,
    SuggestionGenerator,
    SummaryGenerator,
)

router = APIRouter(prefix="/api/v1", tags=["CV Analysis"])

MAX_TEXT_LENGTH = 50000  # Giới hạn tối đa 50.000 ký tự cho văn bản CV


def _process_analysis(raw_text: str, algorithm_version: str = "v1") -> CvAnalyzeResponse:
    """
    Hàm phân tích cốt lõi từ văn bản CV đã được Spring Boot trích xuất bằng PDFBox.
    """
    if not raw_text or not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung văn bản CV không được để trống"
        )

    clean_raw = raw_text.strip()
    if len(clean_raw) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung văn bản CV quá ngắn (tối thiểu 10 ký tự) để thực hiện phân tích"
        )

    if len(clean_raw) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nội dung văn bản CV vượt quá độ dài tối đa cho phép ({MAX_TEXT_LENGTH} ký tự)"
        )

    # 1. Làm sạch văn bản và phân tách các phần
    cleaned_text = TextCleaner.clean(clean_raw)
    sections = TextCleaner.split_sections(cleaned_text)

    # 2. Nhận diện ngôn ngữ CV ('vi' hoặc 'en')
    detected_lang = LanguageDetector.detect(cleaned_text)

    # 3. Phân tích 8 nhóm tiêu chí (Thang 100)
    personal_info_res = PersonalInfoAnalyzer.analyze(cleaned_text, sections.get("header", ""))
    objective_res = ObjectiveAnalyzer.analyze(cleaned_text, sections.get("objective", ""))
    skill_res = SkillAnalyzer.analyze(cleaned_text, sections.get("skills", ""))
    experience_res = ExperienceAnalyzer.analyze(cleaned_text, sections.get("experience", ""))
    project_res = ProjectAnalyzer.analyze(cleaned_text, sections.get("projects", ""))
    education_res = EducationAnalyzer.analyze(cleaned_text, sections.get("education", ""))
    certificate_res = CertificateAnalyzer.analyze(cleaned_text, sections.get("certificates", ""))
    format_res = FormatAnalyzer.analyze(cleaned_text, sections)

    # 4. Tính điểm tổng và bảng điểm chi tiết 8 tiêu chí (mỗi tiêu chí kèm reason)
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

    # 5. Sinh nhận xét ưu điểm, nhược điểm, gợi ý cải thiện và tóm tắt CV
    feedback = FeedbackGenerator.generate(
        personal_info=personal_info_res,
        objective=objective_res,
        skills=skill_res,
        experience=experience_res,
        projects=project_res,
        education=education_res,
        certificates=certificate_res,
        format_info=format_res,
        quality_score=score_res["qualityScore"],
        language=detected_lang,
    )
    strengths = feedback.get("strengths", [])
    weaknesses = feedback.get("weaknesses", [])
    suggestions = feedback.get("suggestions", [])

    summary = SummaryGenerator.generate(
        personal_info=personal_info_res,
        experience=experience_res,
        skills=skill_res,
        education=education_res,
        projects=project_res,
    )

    # 6. Chuẩn bị DTO phản hồi
    personal_info_dto = PersonalInfo(
        fullName=personal_info_res.get("fullName"),
        email=personal_info_res.get("email"),
        phone=personal_info_res.get("phone"),
        location=personal_info_res.get("location"),
        links=personal_info_res.get("links", []),
    )

    experience_dto = ExperienceDetail(
        yearsExperience=experience_res.get("yearsExperience", 0.0),
        seniority=experience_res.get("seniority", "unknown"),
        jobTitles=experience_res.get("jobTitles", []),
    )

    education_dto = EducationDetail(
        educationLevel=education_res.get("educationLevel", "dai_hoc"),
        university=education_res.get("university"),
    )

    project_dto = ProjectDetail(
        hasProjects=bool(project_res.get("details", {}).get("hasProjects")),
        metricsFound=project_res.get("metricsFound", []),
        metricsCount=project_res.get("metricsCount", 0),
    )

    return CvAnalyzeResponse(
        success=True,
        qualityScore=score_res["qualityScore"],
        scoring=score_res["scoring"],
        personalInfo=personal_info_dto,
        skills=skill_res.get("skills", []),
        experience=experience_dto,
        education=education_dto,
        projects=project_dto,
        certificates=certificate_res.get("certificates", []),
        summary=summary,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
        language=detected_lang,
        algorithmVersion=algorithm_version or settings.ALGORITHM_VERSION,
    )


@router.post("/analyze-cv", response_model=CvAnalyzeResponse)
def analyze_cv(request: AnalyzeCvRequest):
    """
    Tiếp nhận văn bản CV từ Spring Boot Backend (sau khi đã trích xuất bằng PDFBox),
    phân tích nội dung và trả về bảng chấm điểm chất lượng 100 điểm kèm gợi ý.
    """
    return _process_analysis(request.text, request.algorithmVersion or settings.ALGORITHM_VERSION)


@router.post("/cv/analyze", response_model=CvAnalyzeResponse)
def analyze_cv_alias(request: AnalyzeCvRequest):
    """
    Alias endpoint cho /api/v1/analyze-cv.
    """
    return _process_analysis(request.text, request.algorithmVersion or settings.ALGORITHM_VERSION)
