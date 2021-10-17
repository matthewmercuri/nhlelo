from data import get_pre_elo_df
from elo import elo_calculator, update_elo
from elo_primer import get_starting_elo_dict


class EloSystem:
    """
    Eventually may want to load dict from cache
    """

    TEAM_ELO_MAP = get_starting_elo_dict()

    @staticmethod
    def _get_pre_elo_df():
        df = get_pre_elo_df()
        df[["Away_ELO", "Home_ELO"]] = 0
        df[["Away_Win_Prob", "Home_Win_Prob"]] = 0
        return df

    @classmethod
    def _add_elos(cls, row):
        away = row["Away"]
        home = row["Home"]

        row[["Away_ELO", "Home_ELO"]] = cls.TEAM_ELO_MAP[away], cls.TEAM_ELO_MAP[home]

        return row

    @classmethod
    def _process_game(cls, row):
        if (row["Away_Goals"] == 0) and (row["Home_Goals"] == 0):
            win_prob_away, win_prob_home = elo_calculator(
                row["Away_ELO"], row["Home_ELO"], row["Away_B2B"], row["Home_B2B"]
            )
            row[["Away_Win_Prob", "Home_Win_Prob"]] = win_prob_away, win_prob_home
        else:
            if row["Away_Goals"] > row["Home_Goals"]:
                away_win = 1
            else:
                away_win = 0

            away_team_elo, home_team_elo = update_elo(
                row["Away_ELO"],
                row["Home_ELO"],
                row["Away_B2B"],
                row["Home_B2B"],
                away_win,
            )

            row[["Away_ELO", "Home_ELO"]] = away_team_elo, home_team_elo
            row[["Away_Win_Prob", "Home_Win_Prob"]] = away_win, (1 - away_win)
            cls.TEAM_ELO_MAP[row["Away"]] = away_team_elo
            cls.TEAM_ELO_MAP[row["Home"]] = home_team_elo

        return row

    @classmethod
    def process_elo_df(cls):
        df = cls._get_pre_elo_df()
        df = df.apply(cls._add_elos, axis=1)
        df = df.apply(cls._process_game, axis=1)
        df.to_csv("save.csv")


EloSystem.process_elo_df()