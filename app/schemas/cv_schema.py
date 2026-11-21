from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AnalyzeCvRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=100000,
        description="Nội dung văn bản CV đã được trích xuất từ PDF bằng PDFBox"
    )
    algorithmVersion: Optional[str] = Field(
        default="v1",
        description="Phiên bản thuật toán đánh giá"
    )


class ScoringItem(BaseModel):
    score: float = Field(..., ge=0.0, description="Điểm số đạt được")
    maxScore: float = Field(..., ge=0.0, description="Điểm số tối đa của tiêu chí")
    reason: str = Field(..., description="Giải thích cụ thể vì sao nhận được số điểm này")


class ScoringDetail(BaseModel):
    personalInfo: ScoringItem
    introduction: ScoringItem
    skills: ScoringItem
    experience: ScoringItem
    projects: ScoringItem
    education: ScoringItem
    certificates: ScoringItem
    format: ScoringItem


class PersonalInfo(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    links: List[str] = []


class ExperienceDetail(BaseModel):
    yearsExperience: float = 0.0
    seniority: str = "unknown"
    jobTitles: List[str] = []


class EducationDetail(BaseModel):
    educationLevel: str = "dai_hoc"
    university: Optional[str] = None


class ProjectDetail(BaseModel):
    hasProjects: bool = False
    metricsFound: List[str] = []
    metricsCount: int = 0


class CvAnalyzeResponse(BaseModel):
    success: bool = True
    qualityScore: float = Field(..., ge=0.0, le=100.0, description="Điểm tổng thể CV (0 - 100)")
    scoring: ScoringDetail
    personalInfo: PersonalInfo
    skills: List[str] = []
    experience: ExperienceDetail
    education: EducationDetail
    projects: ProjectDetail
    certificates: List[str] = []
    summary: str = Field(..., description="Tóm tắt nội dung hồ sơ ứng viên")
    strengths: List[str] = Field(default_factory=list, description="Danh sách ưu điểm nổi bật của CV")
    weaknesses: List[str] = Field(default_factory=list, description="Danh sách nhược điểm hoặc hạn chế cần lưu ý")
    suggestions: List[str] = Field(default_factory=list, description="Danh sách gợi ý cải thiện cụ thể")
    language: str = Field(default="vi", description="Ngôn ngữ chính nhận diện ('vi' hoặc 'en')")
    algorithmVersion: str = Field(default="v1")


class HealthResponse(BaseModel):
    status: str = "UP"
    service: str = "ai-service-check-cv"
    version: str = "1.0.0"
