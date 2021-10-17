import datetime
import numpy as np
import pandas as pd
import requests

"""
API DOCUMENTATION:
https://gitlab.com/dword4/nhlapi/-/tree/master

NOTES:
- may want to break this up into classes with static methods eventually
"""

BASE_URL = "https://statsapi.web.nhl.com/api/v1/"
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")


def _current_season() -> str:
    today = datetime.datetime.today()
    today_year = today.year
    today_month = today.month

    if today_month >= 6:
        other_season_year = today_year + 1
        return str(f"{today_year}{other_season_year}")
    else:
        other_season_year = today_year - 1
        return str(f"{other_season_year}{today_year}")


def _back_to_back(row, schedule_df):
    game_date = row["Date"]
    prev_day = game_date - datetime.timedelta(1)
    away_team = row["Away"]
    home_team = row["Home"]

    prev_date_df = schedule_df[schedule_df["Date"] == prev_day]

    prev_date_away_teams = prev_date_df["Away"].tolist()
    prev_date_home_teams = prev_date_df["Home"].tolist()
    prev_date_teams = prev_date_away_teams + prev_date_home_teams

    if away_team in prev_date_teams:
        row["Away_B2B"] = 1
    if home_team in prev_date_teams:
        row["Home_B2B"] = 1

    return row


def get_schedule_results():
    """
    dates_data is a list (array):
    - each day is its on list item (object)
    - keys:
        - date
        - totalItems
        - toalEvents
        - totalGames
        - totalMatches
        - games: obj containing games
    """

    _url = BASE_URL + "/schedule?season=" + _current_season()
    r = requests.get(_url)
    data = r.json()

    dates_data = data["dates"]

    return dates_data


def get_pre_elo_df(save_locally: bool = False) -> pd.DataFrame:
    """
    Returns the df to be used for elo calculation
    """
    data = {}
    dates_data = get_schedule_results()

    for i, day_data in enumerate(dates_data):
        for j, game_data in enumerate(day_data["games"]):
            if game_data["gameType"] != "PR":
                game_data_dict = {}
                game_data_dict["Date"] = day_data["date"]
                game_data_dict["Away"] = game_data["teams"]["away"]["team"]["name"]
                game_data_dict["Away_Goals"] = game_data["teams"]["away"]["score"]
                game_data_dict["Home"] = game_data["teams"]["home"]["team"]["name"]
                game_data_dict["Home_Goals"] = game_data["teams"]["home"]["score"]
                data[f"{i},{j}"] = game_data_dict

    df = pd.DataFrame.from_dict(data, orient="index")
    df["MOV"] = np.absolute(df["Away_Goals"] - df["Home_Goals"])
    df["Date"] = pd.to_datetime(df["Date"])

    df[["Away_B2B", "Home_B2B"]] = 0
    df = df.apply(_back_to_back, axis=1, schedule_df=df)

    if save_locally:
        df.to_csv("backend/data/CurrentScheduleResults.csv")

    return df


def get_current_teams_list() -> list:
    df = get_pre_elo_df()
    teams = list(set(df["Home"].tolist()))

    return teams
