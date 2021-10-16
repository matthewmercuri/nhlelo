K_FACTOR = 16
HOME_ADJ = 5
B2B_ADJ = 5


def elo_calculator(
    away_team_elo: int, home_team_elo: int, team_map: dict = None
) -> tuple[int, int]:
    expected_score_away = 1 / (1 + (10 ** ((home_team_elo - away_team_elo) / 400)))
    expected_score_home = 1 - expected_score_away

    return away_team_elo, home_team_elo
