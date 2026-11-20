import json
import os
import re
from typing import Dict, Any, List, Set
from rapidfuzz import fuzz


class SkillAnalyzer:
    _skills_dict: Dict[str, List[str]] = {}
    _synonyms: Dict[str, str] = {}

    @classmethod
    def _load_data(cls):
        if not cls._skills_dict:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            data_file = os.path.join(base_dir, "data", "skills_dictionary.json")
            if os.path.exists(data_file):
                with open(data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls._skills_dict = data.get("skills", {})

        if not cls._synonyms:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            syn_file = os.path.join(base_dir, "data", "skill_synonyms.json")
            if os.path.exists(syn_file):
                with open(syn_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls._synonyms = data.get("synonyms", {})

    @classmethod
    def analyze(cls, text: str, skill_section_text: str = "") -> Dict[str, Any]:
        """
        Phân tích kỹ năng chuyên môn từ nội dung CV (Tối đa 20đ).
        """
        cls._load_data()
        low_text = text.lower()
        extracted_skills: Set[str] = set()
        matched_categories: Set[str] = set()
        grouped_skills: Dict[str, List[str]] = {}

        # 1. Quét từ điển kỹ năng bằng Regex Unicode Word Boundary
        for category, skill_list in cls._skills_dict.items():
            cat_found = []
            for skill in skill_list:
                s_lower = skill.lower()
                # Đối với kỹ năng ngắn như c, r, go -> cần kiểm tra chặt chẽ biên từ Unicode
                if len(s_lower) <= 2:
                    pattern = r"(?<![\w#+])" + re.escape(s_lower) + r"(?![\w#+])"
                else:
                    pattern = r"(?<!\w)" + re.escape(s_lower) + r"(?!\w)"

                if re.search(pattern, low_text, re.UNICODE):
                    canonical_name = cls._synonyms.get(s_lower, s_lower)
                    extracted_skills.add(canonical_name)
                    cat_found.append(canonical_name)

            if cat_found:
                matched_categories.add(category)
                grouped_skills[category] = sorted(list(set(cat_found)))

        all_skills = sorted(list(extracted_skills))
        skill_count = len(all_skills)

        # 2. Tính điểm kỹ năng (Tối đa 20.0đ)
        # - Số lượng kỹ năng (tối đa 10.0đ): >=8 skills (10đ), 5-7 (8đ), 3-4 (6đ), 1-2 (3đ)
        # - Độ phủ danh mục chuyên môn (tối đa 5.0đ): >=3 nhóm (5đ), 2 nhóm (3.5đ), 1 nhóm (2đ)
        # - Có section kỹ năng rõ ràng trong CV (tối đa 5.0đ): 5đ nếu có section riêng
        score = 0.0
        details = {}

        # Phần 1: Số lượng
        if skill_count >= 8:
            qty_score = 10.0
        elif skill_count >= 5:
            qty_score = 8.0
        elif skill_count >= 3:
            qty_score = 6.0
        elif skill_count >= 1:
            qty_score = 3.0
        else:
            qty_score = 0.0

        score += qty_score
        details["quantityScore"] = qty_score
        details["skillCount"] = skill_count

        # Phần 2: Đa dạng nhóm
        cat_count = len(matched_categories)
        if cat_count >= 3:
            div_score = 5.0
        elif cat_count >= 2:
            div_score = 3.5
        elif cat_count >= 1:
            div_score = 2.0
        else:
            div_score = 0.0

        score += div_score
        details["diversityScore"] = div_score
        details["categoriesCount"] = cat_count

        # Phần 3: Trình bày mục kỹ năng riêng
        has_skill_sec = bool(skill_section_text and len(skill_section_text.strip()) > 20)
        sec_score = 5.0 if has_skill_sec else (2.5 if skill_count >= 4 else 0.0)
        score += sec_score
        details["sectionScore"] = sec_score

        return {
            "score": min(score, 20.0),
            "skills": all_skills,
            "groupedSkills": grouped_skills,
            "categories": list(matched_categories),
            "details": details
        }
