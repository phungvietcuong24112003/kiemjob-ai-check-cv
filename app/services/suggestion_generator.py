from typing import Dict, Any, List
from app.services.feedback_generator import FeedbackGenerator


class SuggestionGenerator:
    @classmethod
    def generate(
        cls,
        personal_info: Dict[str, Any],
        objective: Dict[str, Any],
        skills: Dict[str, Any],
        experience: Dict[str, Any],
        projects: Dict[str, Any],
        education: Dict[str, Any],
        certificates: Dict[str, Any],
        format_info: Dict[str, Any],
        quality_score: float = 0.0,
        language: str = "vi"
    ) -> List[str]:
        """
        Sinh danh sách các gợi ý cải thiện thiết thực, hành động được (Actionable Suggestions)
        dựa trên FeedbackGenerator.
        """
        feedback = FeedbackGenerator.generate(
            personal_info=personal_info,
            objective=objective,
            skills=skills,
            experience=experience,
            projects=projects,
            education=education,
            certificates=certificates,
            format_info=format_info,
            quality_score=quality_score,
            language=language
        )
        return feedback.get("suggestions", [])

