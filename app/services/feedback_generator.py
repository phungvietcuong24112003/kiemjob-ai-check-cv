from typing import Dict, Any, List


class FeedbackGenerator:
    """
    Module sinh bộ ba nhận xét chuyên sâu:
    1. Ưu điểm nổi bật (Strengths)
    2. Hạn chế cần lưu ý (Weaknesses)
    3. Đề xuất cải thiện (Suggestions)

    Nguyên tắc vàng:
    1. Căn cứ trên dữ liệu thực tế (Factual Evidence)
    2. Không quy chụp năng lực (Fairness)
    3. Tính độc lập & không mâu thuẫn (Mutual Exclusion)
    4. Đa ngôn ngữ (Bilingual 'vi' & 'en')
    5. An toàn kiểu dữ liệu (Luôn là List[str])
    """

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
    ) -> Dict[str, List[str]]:
        lang = (language or "vi").lower()
        is_en = lang.startswith("en")

        strengths: List[str] = []
        weaknesses: List[str] = []
        suggestions: List[str] = []

        # =========================================================================
        # 1. THÔNG TIN CÁ NHÂN & LIÊN HỆ (Personal Info)
        # =========================================================================
        has_phone = bool(personal_info.get("phone"))
        has_email = bool(personal_info.get("email"))
        links = personal_info.get("links", [])
        has_links = bool(links and len(links) > 0)
        has_location = bool(personal_info.get("location"))

        if has_phone and has_email and (has_links or has_location):
            if is_en:
                strengths.append("Complete contact and personal details provided, including professional channels.")
            else:
                strengths.append("Thông tin cá nhân và phương thức liên hệ đầy đủ, rõ ràng và chuyên nghiệp.")
        elif not has_phone or not has_email:
            missing_items = []
            if not has_phone:
                missing_items.append("phone number" if is_en else "số điện thoại")
            if not has_email:
                missing_items.append("email" if is_en else "địa chỉ email")

            if is_en:
                weaknesses.append(f"Missing essential direct contact information: {', '.join(missing_items)}.")
                suggestions.append("Add your active phone number and a professional email address for quick recruiter reach.")
            else:
                weaknesses.append(f"Hồ sơ còn thiếu phương thức liên hệ cơ bản: {', '.join(missing_items)}.")
                suggestions.append("Bổ sung số điện thoại và địa chỉ email chính xác để nhà tuyển dụng có thể liên hệ phỏng vấn nhanh chóng.")
        elif not has_links:
            if is_en:
                weaknesses.append("No links to online professional profiles (such as LinkedIn, GitHub, or personal portfolio).")
                suggestions.append("Include links to your LinkedIn profile, GitHub repositories, or online portfolio to showcase verified work.")
            else:
                weaknesses.append("Chưa đính kèm liên kết hồ sơ chuyên môn (LinkedIn, GitHub hoặc Portfolio cá nhân).")
                suggestions.append("Nên bổ sung liên kết đến trang LinkedIn hoặc GitHub/Portfolio để tăng độ tin cậy và minh chứng năng lực thực tế.")

        # =========================================================================
        # 2. MỤC TIÊU NGHỀ NGHIỆP / GIỚI THIỆU (Objective / Summary)
        # =========================================================================
        obj_words = objective.get("wordCount", 0)
        obj_score = float(objective.get("score", 0.0))

        if obj_words >= 25 and obj_score >= 7.0:
            if is_en:
                strengths.append("Clear professional summary and career objective outlining domain focus and direction.")
            else:
                strengths.append("Phần giới thiệu bản thân và mục tiêu nghề nghiệp rõ ràng, định hướng chuyên môn mạch lạc.")
        elif obj_words < 15:
            if is_en:
                weaknesses.append("Career objective or professional summary is missing or too brief.")
                suggestions.append("Add a concise professional summary (30-80 words) describing your core background and value proposition.")
            else:
                weaknesses.append("Phần giới thiệu bản thân hoặc mục tiêu nghề nghiệp còn thiếu hoặc quá ngắn.")
                suggestions.append("Bổ sung phần 'Mục tiêu nghề nghiệp' (khoảng 30-80 từ) nêu rõ định hướng chuyên môn và giá trị bạn mong muốn đóng góp cho công ty.")
        elif obj_words < 25:
            if is_en:
                weaknesses.append("Career objective is somewhat brief and could articulate long-term goals more clearly.")
                suggestions.append("Expand your career objective to highlight key technical strengths and 1-2 year development goals.")
            else:
                weaknesses.append("Phần mục tiêu nghề nghiệp còn khá ngắn, chưa làm nổi bật định hướng dài hạn.")
                suggestions.append("Mở rộng thêm phần mục tiêu nghề nghiệp, tập trung vào kỹ năng chuyên sâu và định hướng phát triển trong 1-2 năm tới.")

        # =========================================================================
        # 3. KỸ NĂNG CHUYÊN MÔN (Skills)
        # =========================================================================
        skill_list = skills.get("skills", [])
        skill_count = len(skill_list)
        categories = skills.get("categories", [])

        if skill_count >= 6:
            if is_en:
                strengths.append(f"Diverse technical skill set ({skill_count} relevant skills recognized) aligned with modern demands.")
            else:
                strengths.append(f"Kỹ năng chuyên môn phong phú ({skill_count} kỹ năng được nhận diện) và phù hợp với định hướng công việc.")
        elif skill_count < 3:
            if is_en:
                weaknesses.append("Identified skill set is limited (fewer than 3 skills recognized from the text).")
                suggestions.append("List more core programming languages, frameworks, databases, and relevant tools you have worked with.")
            else:
                weaknesses.append("Số lượng kỹ năng chuyên môn còn ít (dưới 3 kỹ năng được nhận diện trong hồ sơ).")
                suggestions.append("Liệt kê đầy đủ hơn các ngôn ngữ lập trình, framework, cơ sở dữ liệu và công cụ hỗ trợ bạn đã sử dụng.")
        elif skill_count >= 4 and len(categories) <= 1:
            if is_en:
                weaknesses.append("Skills are listed without clear categorization by domain or technology stack.")
                suggestions.append("Group your technical skills into distinct categories (e.g., Languages, Frameworks, Databases, Tools).")
            else:
                weaknesses.append("Các kỹ năng chuyên môn chưa được phân nhóm theo danh mục rõ ràng.")
                suggestions.append("Nên phân loại kỹ năng thành các nhóm rõ ràng (ví dụ: Ngôn ngữ lập trình, Frameworks, Cơ sở dữ liệu, Công cụ làm việc).")

        # =========================================================================
        # 4. KINH NGHIỆM LÀM VIỆC (Experience)
        # =========================================================================
        has_exp = experience.get("hasExperience", False)
        years_exp = float(experience.get("yearsExperience", 0.0))
        exp_score = float(experience.get("score", 0.0))

        if has_exp and years_exp >= 1.0 and exp_score >= 12.0:
            if is_en:
                strengths.append(f"Solid work history ({years_exp} years estimated) with structured timeline and job responsibilities.")
            else:
                strengths.append(f"Kinh nghiệm làm việc có các mốc thời gian rõ ràng (~{years_exp} năm kinh nghiệm), thể hiện quá trình công tác ổn định.")
        elif not has_exp or exp_score < 8.0:
            if is_en:
                weaknesses.append("Work experience section is brief or lacks specific employment timelines.")
                suggestions.append("Provide clear employment dates (Month/Year), company names, and bullet points of your primary duties.")
            else:
                weaknesses.append("Thông tin kinh nghiệm làm việc còn ít hoặc chưa có mốc thời gian công tác cụ thể.")
                suggestions.append("Bổ sung chi tiết các vị trí công việc đã trải qua kèm mốc thời gian (Tháng/Năm) và tóm tắt 3-5 nhiệm vụ trọng tâm.")

        # =========================================================================
        # 5. DỰ ÁN THỰC TẾ & ĐỊNH LƯỢNG (Projects & Metrics)
        # =========================================================================
        has_projects = bool(projects.get("details", {}).get("hasProjects"))
        metrics_found = projects.get("metricsFound", [])
        metrics_count = len(metrics_found) if metrics_found else projects.get("metricsCount", 0)

        if has_projects and metrics_count >= 1:
            if is_en:
                strengths.append("Hands-on projects feature concrete quantitative metrics demonstrating practical impact.")
            else:
                strengths.append("Dự án thực tế được trình bày rõ ràng và có số liệu định lượng thành tích cụ thể.")
        elif not has_projects:
            if is_en:
                weaknesses.append("No dedicated projects section found to showcase practical implementation skills.")
                suggestions.append("Add a 'Featured Projects' section describing technologies used, problems solved, and your individual role.")
            else:
                weaknesses.append("Chưa có mục dự án thực tế riêng biệt để chứng minh năng lực triển khai sản phẩm.")
                suggestions.append("Nên bổ sung mục 'Dự án nổi bật' mô tả công nghệ sử dụng, bài toán giải quyết và vai trò cá nhân.")
        else:
            # has_projects is True, but metrics_count == 0
            if is_en:
                weaknesses.append("Project descriptions currently lack quantitative outcomes or measurable results.")
                suggestions.append("Incorporate quantifiable impact into your projects (e.g., '% performance improvement', 'user volume', 'sales growth').")
            else:
                weaknesses.append("Mô tả dự án chưa thể hiện số liệu định lượng hoặc kết quả đo lường thành tích thực tế.")
                suggestions.append("Bổ sung các con số kết quả thực tế nếu có (ví dụ: '% tối ưu tốc độ', 'số lượng người dùng', 'đạt chỉ tiêu').")

        # =========================================================================
        # 6. HỌC VẤN (Education)
        # =========================================================================
        university = education.get("university")
        edu_score = float(education.get("score", 0.0))

        if university or edu_score >= 8.0:
            uni_name = f" ({university})" if university else ""
            if is_en:
                strengths.append(f"Clear higher education credentials{uni_name} from a recognized institution.")
            else:
                strengths.append(f"Học vấn đạt trình độ chuẩn mực{uni_name} tại cơ sở đào tạo chuyên ngành.")
        elif edu_score < 6.0 and not university:
            if is_en:
                weaknesses.append("Education section lacks details regarding university or degree major.")
                suggestions.append("Specify your higher education institution, degree major, and graduation year.")
            else:
                weaknesses.append("Thông tin cơ sở đào tạo hoặc chuyên ngành học vấn chưa được nêu cụ thể.")
                suggestions.append("Nêu rõ tên trường Đại học/Cao đẳng, chuyên ngành theo học và năm tốt nghiệp (hoặc dự kiến tốt nghiệp).")

        # =========================================================================
        # 7. CHỨNG CHỈ & NGOẠI NGỮ (Certificates)
        # =========================================================================
        certs = certificates.get("certificates", [])
        cert_count = len(certs)

        if cert_count >= 1:
            if is_en:
                strengths.append(f"Includes verified certifications ({cert_count} credential(s) listed), strengthening competitive edge.")
            else:
                strengths.append(f"Có chứng chỉ chuyên môn hoặc ngoại ngữ bổ trợ ({cert_count} chứng chỉ), tạo điểm cộng uy tín cho hồ sơ.")
        elif quality_score < 80.0 and len(weaknesses) < 4:
            # Chỉ gợi ý bổ sung chứng chỉ khi hồ sơ tổng thể chưa đạt mức điểm xuất sắc
            if is_en:
                weaknesses.append("No professional credentials or foreign language certifications listed.")
                suggestions.append("Add relevant professional certifications (e.g. AWS, Java, Scrum) or language scores (TOEIC, IELTS) if available.")
            else:
                weaknesses.append("Chưa liệt kê chứng chỉ chuyên môn hoặc ngoại ngữ bổ trợ.")
                suggestions.append("Bổ sung các chứng chỉ chuyên môn (AWS, Java, Scrum...) hoặc chứng chỉ ngoại ngữ (TOEIC, IELTS) nếu có để gia tăng sức cạnh tranh.")

        # =========================================================================
        # 8. CẤU TRÚC & ĐỊNH DẠNG (Format)
        # =========================================================================
        word_count = format_info.get("wordCount", 0)
        sections_count = format_info.get("sectionsCount", 0)

        if 350 <= word_count <= 1600 and sections_count >= 4:
            if is_en:
                strengths.append("Well-balanced document length and layout structure with distinct logical sections.")
            else:
                strengths.append("Bố cục CV có cấu trúc hợp lý, độ dài cân đối và dễ dàng cho nhà tuyển dụng quét thông tin.")
        elif word_count < 250:
            if is_en:
                weaknesses.append("Overall content length is quite short (under 250 words), which may leave out key qualifications.")
                suggestions.append("Flesh out details in your project and experience sections to make the resume more comprehensive.")
            else:
                weaknesses.append("Nội dung CV quá ngắn (dưới 250 từ), chưa thể hiện đầy đủ các kinh nghiệm và năng lực chuyên môn.")
                suggestions.append("Phát triển thêm nội dung cho phần dự án và mô tả nhiệm vụ công việc để CV đầy đặn và thuyết phục hơn.")
        elif word_count > 1800:
            if is_en:
                weaknesses.append("CV length exceeds 1800 words, which can be overly lengthy for quick recruiter screening.")
                suggestions.append("Condense your resume to 1-2 standard pages, highlighting only the most impactful accomplishments.")
            else:
                weaknesses.append("Độ dài CV hơi dài (trên 1800 từ), có thể gây khó khăn cho nhà tuyển dụng khi quét nhanh hồ sơ.")
                suggestions.append("Nên cô đọng lại khoảng 1-2 trang tiêu chuẩn, ưu tiên những kinh nghiệm và thành tích nổi bật nhất.")

        # =========================================================================
        # Fallback bảo đảm không rỗng
        # =========================================================================
        if not strengths and quality_score >= 40.0:
            if is_en:
                strengths.append("Basic candidate information and skills structure are established.")
            else:
                strengths.append("Hồ sơ đã bước đầu thiết lập được khung thông tin cá nhân và định hướng nghề nghiệp.")

        if not suggestions:
            if is_en:
                suggestions.append("Your CV is already well-structured! Continue keeping your latest technical achievements updated.")
                suggestions.append("Review spelling and visual consistency before sending applications.")
            else:
                suggestions.append("Hồ sơ của bạn đã có cấu trúc rất tốt! Hãy tiếp tục duy trì cập nhật các công nghệ và dự án mới nhất.")
                suggestions.append("Kiểm tra lại chính tả và cách trình bày font chữ đồng bộ trước khi gửi ứng tuyển.")

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions[:6],  # Tối đa 6 đề xuất hành động trọng tâm
        }
