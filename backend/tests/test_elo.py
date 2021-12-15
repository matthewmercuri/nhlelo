from app.elo import elo_calculator, update_elo

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


def test_update_elo():
    away_team_elo, home_team_elo = update_elo(1500, 1500, 0, 0, 0)
    assert away_team_elo == 1492.528
    assert home_team_elo == 1507.472

    away_team_elo, home_team_elo = update_elo(1500, 1500, 0, 0, 1)
    assert away_team_elo == 1508.528
    assert home_team_elo == 1491.472
