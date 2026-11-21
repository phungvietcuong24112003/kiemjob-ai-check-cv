from app.services.score_calculator import ScoreCalculator


def test_score_calculator_total():
    p = {"score": 10.0}
    o = {"score": 8.0}
    s = {"score": 18.0}
    e = {"score": 16.0}
    proj = {"score": 15.0}
    edu = {"score": 9.0}
    cert = {"score": 4.0}
    fmt = {"score": 5.0}

    res = ScoreCalculator.calculate_total(p, o, s, e, proj, edu, cert, fmt)
    assert res["qualityScore"] == 85.0
    assert res["scoring"].personalInfo.score == 10.0
    assert res["scoring"].skills.score == 18.0
    assert res["scoring"].personalInfo.maxScore == 10.0
    assert len(res["scoring"].personalInfo.reason) > 0


def test_score_calculator_bounds():
    # Test vượt trần
    p = {"score": 99.0}
    o = {"score": 99.0}
    s = {"score": 99.0}
    e = {"score": 99.0}
    proj = {"score": 99.0}
    edu = {"score": 99.0}
    cert = {"score": 99.0}
    fmt = {"score": 99.0}

    res = ScoreCalculator.calculate_total(p, o, s, e, proj, edu, cert, fmt)
    assert res["qualityScore"] == 100.0
    assert res["scoring"].personalInfo.score == 10.0
