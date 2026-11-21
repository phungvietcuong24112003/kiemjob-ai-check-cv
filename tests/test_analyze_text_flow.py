import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_cvs")


def _load_sample(filename: str) -> dict:
    filepath = os.path.join(SAMPLE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"
    assert res.json()["service"] == "ai-service-check-cv"


def test_sample_1_good_full():
    payload = _load_sample("sample_1_good_full.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["success"] is True
    assert data["qualityScore"] >= 85.0
    assert data["language"] == "vi"
    assert "java" in [s.lower() for s in data["skills"]]

    # Kiểm tra tổng điểm thành phần khớp chính xác với điểm tổng
    scoring = data["scoring"]
    sum_scores = sum(item["score"] for item in scoring.values())
    assert round(sum_scores, 1) == data["qualityScore"]

    # Kiểm tra 8 mục đều có điểm và lý do giải thích
    for key, item in scoring.items():
        assert "score" in item
        assert "maxScore" in item
        assert "reason" in item
        assert len(item["reason"]) > 5


def test_sample_2_missing_contact():
    payload = _load_sample("sample_2_missing_contact.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert any("số điện thoại" in s.lower() for s in data["suggestions"])


def test_sample_3_fresher_education():
    payload = _load_sample("sample_3_fresher_education_only.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scoring"]["education"]["score"] == 10.0


def test_sample_4_many_projects():
    payload = _load_sample("sample_4_many_projects.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scoring"]["projects"]["score"] >= 18.0
    assert data["projects"]["metricsCount"] >= 3


def test_sample_5_english():
    payload = _load_sample("sample_5_english.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["language"] == "en"
    assert "react" in [s.lower() for s in data["skills"]]


def test_sample_6_vietnamese():
    payload = _load_sample("sample_6_vietnamese.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "misa" in [s.lower() for s in data["skills"]]


def test_sample_7_short():
    payload = _load_sample("sample_7_short.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["qualityScore"] < 50.0
    assert any("ngắn" in s.lower() or "bổ sung" in s.lower() for s in data["suggestions"])


def test_sample_8_unrelated():
    payload = _load_sample("sample_8_unrelated.json")
    res = client.post("/api/v1/analyze-cv", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["qualityScore"] < 25.0


def test_empty_text():
    res = client.post("/api/v1/analyze-cv", json={"text": ""})
    assert res.status_code in (400, 422)


def test_too_short_text():
    res = client.post("/api/v1/analyze-cv", json={"text": "Ngắn"})
    assert res.status_code in (400, 422)


def test_too_long_text():
    super_long_text = "Java developer Spring Boot " * 5000  # > 100.000 ký tự
    res = client.post("/api/v1/analyze-cv", json={"text": super_long_text})
    assert res.status_code in (400, 422)


def test_missing_text_field():
    res = client.post("/api/v1/analyze-cv", json={"algorithmVersion": "v1"})
    assert res.status_code == 422
