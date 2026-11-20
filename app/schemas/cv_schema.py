from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CvAnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Nội dung văn bản CV đã được trích xuất từ PDF hoặc form nhập"
    )


class ScoringBreakdown(BaseModel):
    personalInfoScore: float = Field(..., ge=0.0, le=10.0, description="Điểm thông tin cá nhân & liên hệ (tối đa 10)")
    objectiveScore: float = Field(..., ge=0.0, le=10.0, description="Điểm mục tiêu nghề nghiệp / giới thiệu (tối đa 10)")
    skillScore: float = Field(..., ge=0.0, le=20.0, description="Điểm kỹ năng chuyên môn (tối đa 20)")
    experienceScore: float = Field(..., ge=0.0, le=20.0, description="Điểm kinh nghiệm làm việc (tối đa 20)")
    projectScore: float = Field(..., ge=0.0, le=20.0, description="Điểm dự án thực tế (tối đa 20)")
    educationScore: float = Field(..., ge=0.0, le=10.0, description="Điểm học vấn (tối đa 10)")
    certificateScore: float = Field(..., ge=0.0, le=5.0, description="Điểm chứng chỉ & thành tích (tối đa 5)")
    formatScore: float = Field(..., ge=0.0, le=5.0, description="Điểm cấu trúc & định dạng (tối đa 5)")


class PersonalInfo(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    links: List[str] = []


class SearchProfile(BaseModel):
    jobTitles: List[str] = []
    skills: List[str] = []
    yearsExperience: float = 0.0
    seniority: str = "unknown"
    educationLevel: str = "dai_hoc"
    industry: str = "Công nghệ thông tin"


class ParsedCvData(BaseModel):
    scoring: ScoringBreakdown
    personalInfo: PersonalInfo
    searchProfile: SearchProfile
    details: Dict[str, Any] = {}


class CvAnalyzeResponse(BaseModel):
    qualityScore: float = Field(..., ge=0.0, le=100.0, description="Điểm tổng thể chất lượng CV trên thang 100")
    summary: str = Field(..., description="Tóm tắt nội dung hồ sơ ứng viên")
    suggestions: List[str] = Field(..., description="Danh sách các gợi ý cải thiện cụ thể")
    parsedData: ParsedCvData
    algorithmVersion: str = Field(default="v1-python-rule-based")


class HealthResponse(BaseModel):
    status: str = "UP"
    service: str = "ai-service-check-cv"
    version: str = "1.0.0"
