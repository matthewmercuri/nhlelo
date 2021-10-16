"""
FINDING FACTORS:
- HOME_ADJ: how much more likely is a home team to win vs. an away team?
- B2B_ADJ: how much more likly is a fresh team going to win vs. a team that played yesterday?
- MOV_ADJ?
"""

K_FACTOR = 16
HOME_ADJ = 0.033
B2B_ADJ = 0.10


def elo_calculator(
    away_team_elo: int,
    home_team_elo: int,
    away_b2b: int,
    home_b2b: int,
) -> tuple[float, float]:
    """
    Can use this function alone to calculate win probabilities (game to be played)
    """
    expected_score_away = 1 / (1 + (10 ** ((home_team_elo - away_team_elo) / 400)))

    # adjusting for home ice advantage
    expected_score_away -= HOME_ADJ

    # adjusting for back-to-back
    if (away_b2b == 1) and (home_b2b != 1):
        expected_score_away -= B2B_ADJ
    elif (home_b2b == 1) and (away_b2b != 1):
        expected_score_away += B2B_ADJ

    expected_score_home = 1 - expected_score_away

    return expected_score_away, expected_score_home


def update_elo(
    away_team_elo: int,
    home_team_elo: int,
    away_b2b: int,
    home_b2b: int,
    away_win: int,
    team_map: dict = None,
) -> tuple[int, int]:
    """
    TODO:
    - update 'team map' if provided (insert new ELOs)
    """

    expected_score_away, expected_score_home = elo_calculator(
        away_team_elo, home_team_elo, away_b2b, home_b2b
    )

    home_win = 1 - away_win

    away_team_elo += K_FACTOR * (away_win - expected_score_away)
    home_team_elo += K_FACTOR * (home_win - expected_score_home)

    return away_team_elo, home_team_elo
