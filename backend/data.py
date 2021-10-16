from datetime import datetime
import json
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

    if today_month >= 5:
        other_season_year = today_year + 1
        return str(f"{today_year}{other_season_year}")
    else:
        other_season_year = today_year - 1
        return str(f"{other_season_year}{today_year}")


def get_schedule_results():
    _url = BASE_URL + "/schedule?season=" + _current_season()
    r = requests.get(_url)
    data = r.json()

    dates_data = data["dates"]
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

    return dates_data


def get_schedule_results_df():
    data = {}
    dates_data = get_schedule_results()

    for day_data in dates_data:
        data[day_data["date"]] = {}
        # data[day_data["date"]]["games"] = day_data["games"]
        print(day_data["games"][0]["teams"])
        break


get_schedule_results_df()
