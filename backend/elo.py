"""
FINDING FACTORS:
- HOME_ADJ: how much more likely is a home team to win vs. an away team?
- B2B_ADJ: how much more likly is a fresh team going to win vs. a team that played yesterday?
"""

K_FACTOR = 16
HOME_ADJ = 5
B2B_ADJ = 5


def elo_calculator(
    away_team_elo: int, home_team_elo: int, team_map: dict = None
) -> tuple[int, int]:
    expected_score_away = 1 / (1 + (10 ** ((home_team_elo - away_team_elo) / 400)))
    expected_score_home = 1 - expected_score_away

    return away_team_elo, home_team_elo
