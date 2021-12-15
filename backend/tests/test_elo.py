from app.elo import elo_calculator

"""
WD: backend
Command: python -m pytest tests/
"""


def test_elo_calculator():
    expected_score_away, expected_score_home = elo_calculator(1500, 1500, 0, 0)
    assert round(expected_score_away, 3) == 0.467
    assert round(expected_score_home, 3) == 0.533

    expected_score_away, expected_score_home = elo_calculator(1500, 1500, 1, 0)
    assert round(expected_score_away, 3) == 0.367
    assert round(expected_score_home, 3) == 0.633

    expected_score_away, expected_score_home = elo_calculator(1400, 1600, 0, 0)
    assert round(expected_score_away, 3) == 0.207
    assert round(expected_score_home, 3) == 0.793

    expected_score_away, expected_score_home = elo_calculator(1600, 1400, 0, 0)
    assert round(expected_score_away, 3) == 0.727
    assert round(expected_score_home, 3) == 0.273
