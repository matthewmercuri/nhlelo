import pandas as pd
import pytz

from app.elo import elo_calculator, update_elo
from app.nhl_api import NHLAPI

"""
Handles all the necessary data for the API. Should a data
source fail, this provides abstraction so it could take in
any data with the same format as previously used.
"""


class ELOStore:
    """
    Stores all the teams and updates their ELOs
    """

    def __init__(self):
        """
        Reads in initial values and creates dict

        TODO: fix this, inelegant
        """
        self.team_elo_dict = pd.read_csv(
            "./app/starting_elo.csv", index_col=0
        ).to_dict()["0"]

    def set_team_elo(self, team: str, elo: float):
        self.team_elo_dict[team] = elo

    def get_team_elo(self, team: str) -> float:
        return self.team_elo_dict[team]

    def get_team_elo_dict(self) -> dict:
        return self.team_elo_dict


class Data:
    def __init__(self):
        # initializing team ELO store
        self.ELOStore = ELOStore()

    def _prep_schedule_df(self) -> pd.DataFrame:
        df = NHLAPI.get_schedule_df()

        # removing preseaon and all-start games
        df = df[df["gameType"] != "PR"]
        df = df[df["gameType"] != "A"]

        df["date"] = pd.to_datetime(df["date"])
        df["gameEloAway"] = 0
        df["gameEloHome"] = 0
        df["awayB2b"] = 0
        df["homeB2b"] = 0
        df["awayWinProb"] = 0
        df["homeWinProb"] = 0
        df["awayDecimalOdds"] = 0
        df["homeDecimalOdds"] = 0

        return df

    def _is_team_playing_back2back(self, date, df: pd.DataFrame, team: str) -> int:
        yesterday = date + pd.Timedelta(days=-1)
        df = df[(df["awayTeam"] == team) | (df["homeTeam"] == team)]
        df = df[df["status"] == "Final"]

        if yesterday in df["date"].tolist():
            return 1
        else:
            return 0

    def _process_game_row(self, x, df):
        x["gameEloAway"] = self.ELOStore.get_team_elo(x["awayTeam"])
        x["gameEloHome"] = self.ELOStore.get_team_elo(x["homeTeam"])

        is_away_b2b = self._is_team_playing_back2back(x["date"], df, x["awayTeam"])
        x["awayB2b"] = is_away_b2b

        is_home_b2b = self._is_team_playing_back2back(x["date"], df, x["homeTeam"])
        x["homeB2b"] = is_home_b2b

        if x["status"] == "Final":
            if x["awayScore"] > x["homeScore"]:
                x["awayWinProb"], x["homeWinProb"] = 1, -1
                away_win = 1
            else:
                x["awayWinProb"], x["homeWinProb"] = -1, 1
                away_win = 0

            new_away_elo, new_home_elo = update_elo(
                x["gameEloAway"], x["gameEloHome"], is_away_b2b, is_home_b2b, away_win
            )

            self.ELOStore.set_team_elo(x["awayTeam"], new_away_elo)
            self.ELOStore.set_team_elo(x["homeTeam"], new_home_elo)
        else:
            x["awayWinProb"], x["homeWinProb"] = elo_calculator(
                self.ELOStore.get_team_elo(x["awayTeam"]),
                self.ELOStore.get_team_elo(x["homeTeam"]),
                is_away_b2b,
                is_home_b2b,
            )

        return x

    def _post_process_df(self, df):
        # converting dateTimeEst to str because of Mongo, not ideal
        df["dateEst"] = (
            pd.DatetimeIndex(df["date"]).tz_convert("US/Eastern").strftime("%Y-%m-%d")
        )
        df["timeEst"] = (
            pd.DatetimeIndex(df["date"]).tz_convert("US/Eastern").strftime("%H-%M-%S")
        )
        df["awayDecimalOdds"] = 1 / df["awayWinProb"]
        df["homeDecimalOdds"] = 1 / df["homeWinProb"]

        return df

    def process_schedule_df(self) -> pd.DataFrame:
        df = self._prep_schedule_df()
        df = df.apply(self._process_game_row, args=(df,), axis=1)
        df = self._post_process_df(df)

        return df

    def get_team_elos(self) -> pd.DataFrame:
        self.process_schedule_df()

        team_elos_dict = self.ELOStore.get_team_elo_dict()
        df = pd.DataFrame.from_dict(team_elos_dict, orient="index")
        df.sort_values(by=[0], ascending=False, inplace=True)

        return df
