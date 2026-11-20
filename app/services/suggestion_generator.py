from typing import Dict, Any, List


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
        format_info: Dict[str, Any]
    ) -> List[str]:
        """
        Sinh danh sách các gợi ý cải thiện thiết thực, hành động được (Actionable Suggestions)
        dựa trên các điểm yếu thực tế trong CV.
        """
        suggestions: List[str] = []

        # 1. Gợi ý Thông tin liên hệ
        if not personal_info.get("phone"):
            suggestions.append("Bổ sung số điện thoại liên lạc chính xác để nhà tuyển dụng có thể gọi phỏng vấn nhanh chóng.")
        if not personal_info.get("email"):
            suggestions.append("Bổ sung địa chỉ email chuyên nghiệp (ví dụ: hoten@gmail.com).")
        if not personal_info.get("links") or len(personal_info.get("links", [])) == 0:
            suggestions.append("Nên thêm liên kết đến trang cá nhân chuyên nghiệp như LinkedIn hoặc GitHub/Portfolio để tăng độ tin cậy.")

        # 2. Gợi ý Mục tiêu nghề nghiệp
        obj_words = objective.get("wordCount", 0)
        if obj_words < 15:
            suggestions.append("Bổ sung phần 'Mục tiêu nghề nghiệp' (khoảng 30-80 từ) nêu rõ định hướng chuyên môn và giá trị bạn mong muốn đóng góp cho công ty.")
        elif obj_words < 25:
            suggestions.append("Phần mục tiêu nghề nghiệp hơi ngắn. Hãy mở rộng thêm về kế hoạch phát triển kỹ năng và đóng góp cụ thể trong 1-2 năm tới.")

        # 3. Gợi ý Kỹ năng
        skill_count = len(skills.get("skills", []))
        if skill_count < 4:
            suggestions.append("Danh sách kỹ năng còn khá ít. Hãy bổ sung đầy đủ các công cụ, ngôn ngữ, framework và kỹ năng mềm bạn đã sử dụng.")
        elif len(skills.get("categories", [])) <= 1:
            suggestions.append("Nên nhóm các kỹ năng theo danh mục rõ ràng (ví dụ: Chuyên môn, Công cụ làm việc, Kỹ năng mềm) để CV dễ theo dõi.")

        # 4. Gợi ý Dự án & Số liệu định lượng
        metrics_count = projects.get("metricsCount", 0)
        if metrics_count == 0:
            suggestions.append("Phần dự án/kinh nghiệm đang thiếu số liệu định lượng. Hãy bổ sung các con số kết quả cụ thể (ví dụ: 'tối ưu 30% tốc độ tải trang', 'phục vụ 5.000 người dùng', 'đạt 115% chỉ tiêu').")
        
        if not projects.get("details", {}).get("hasProjects"):
            suggestions.append("Nên bổ sung mục 'Dự án nổi bật' mô tả công nghệ sử dụng, vai trò cá nhân và kết quả đạt được để chứng minh năng lực thực tế.")

        # 5. Gợi ý Kinh nghiệm làm việc
        exp_score = experience.get("score", 0.0)
        if exp_score < 10.0:
            suggestions.append("Mô tả chi tiết hơn quá trình làm việc, nêu rõ tên công ty, vị trí, khoảng thời gian (Tháng/Năm) và các nhiệm vụ trọng tâm.")

        # 6. Gợi ý Chứng chỉ
        cert_count = len(certificates.get("certificates", []))
        if cert_count == 0:
            suggestions.append("Bổ sung các chứng chỉ chuyên môn hoặc ngoại ngữ (IELTS, TOEIC, AWS, MOS, chứng chỉ online...) nếu có để tạo lợi thế cạnh tranh.")

        # 7. Gợi ý Định dạng & Độ dài
        word_count = format_info.get("wordCount", 0)
        if word_count < 250:
            suggestions.append("Độ dài CV hiện tại khá ngắn (dưới 250 từ). Hãy phát triển thêm nội dung về dự án và kinh nghiệm để CV thêm đày đặn.")
        elif word_count > 1800:
            suggestions.append("Nội dung CV hơi dài (trên 1800 từ). Nên cô đọng lại khoảng 1-2 trang tiêu chuẩn, tập trung vào những kinh nghiệm và kỹ năng nổi bật nhất.")

        # Đảm bảo có ít nhất 1-2 gợi ý hữu ích
        if not suggestions:
            suggestions.append("Hồ sơ của bạn đã có cấu trúc rất tốt! Hãy tiếp tục duy trì cập nhật các công nghệ và dự án mới nhất.")
            suggestions.append("Kiểm tra lại chính tả và cách trình bày font chữ đồng bộ trước khi gửi ứng tuyển.")

        return suggestions[:6]
