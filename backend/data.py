from datetime import datetime
import pandas as pd
import requests

"""
API DOCUMENTATION:
https://gitlab.com/dword4/nhlapi/-/tree/master
"""

BASE_URL = "https://statsapi.web.nhl.com/api/v1/"
TODAY = datetime.now().strftime("%Y-%m-%d")


def _current_season() -> str:
    today = datetime.today()
    today_year = today.year
    today_month = today.month

    if today_month >= 6:
        other_season_year = today_year + 1
        return str(f"{today_year}{other_season_year}")
    else:
        other_season_year = today_year - 1
        return str(f"{other_season_year}{today_year}")


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


def get_schedule_results_df():
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

    return df


get_schedule_results_df()
