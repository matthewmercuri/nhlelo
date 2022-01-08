import json
import pandas as pd
import requests

"""
This module interacts with the NHL API and transforms the data to be ready
to use by the app.

API Documentation Repo:
https://gitlab.com/dword4/nhlapi
"""

BASE_URL = "https://statsapi.web.nhl.com/api/v1/"
ENDPOINTS = ["schedule", "teams"]


class NHLAPIRaw:
    @staticmethod
    def use_nhl_api(endpoint: str, params: dict = None):
        endpoint = endpoint.strip().lower()

        if endpoint not in ENDPOINTS:
            raise KeyError(f"{endpoint} not in valid endpoints: {ENDPOINTS}")

        try:
            r = requests.get(BASE_URL + endpoint, params=params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except Exception as e:
            print(f"Error communicating with NHL API ({endpoint}). Error: {e}")

        return r.json()

    # TODO: make the season initialize with env variable or auto calculate
    @classmethod
    def get_detailed_schedule(cls, season: int = 20212022):
        request = cls.use_nhl_api("schedule", {"season": season})
        return request["dates"]

    @classmethod
    def get_team_metadata(cls):
        request = cls.use_nhl_api("teams")
        return request["teams"]

    @staticmethod
    def _pretty_print_json(data):
        print(json.dumps(data, indent=2))


class NHLAPI:
    """
    Transforms raw data from the NHLAPIRaw class into usable data
    """

    @staticmethod
    def get_team_names_list() -> list:
        team_metadata = NHLAPIRaw.get_team_metadata()
        return [team_data["name"] for team_data in team_metadata]

    @staticmethod
    def get_schedule_df() -> pd.DataFrame:
        # returns array of day object holding game data
        schedule_raw = NHLAPIRaw.get_detailed_schedule()

        # each day object we need games
        cleaned_data_dict = {}
        for day_object in schedule_raw:
            for i, game_object in enumerate(day_object["games"]):
                cleaned_data_dict[f"{i} {game_object['gameDate']}"] = {
                    "date": game_object["gameDate"],
                    "gameType": game_object["gameType"],
                    "status": game_object["status"]["abstractGameState"],
                    "awayTeam": game_object["teams"]["away"]["team"]["name"],
                    "awayScore": game_object["teams"]["away"]["score"],
                    "homeScore": game_object["teams"]["home"]["score"],
                    "homeTeam": game_object["teams"]["home"]["team"]["name"],
                }

        # converting clean data dict into df
        df = pd.DataFrame.from_dict(cleaned_data_dict, orient="index")

        return df

    @staticmethod
    def get_todays_games_df() -> pd.DataFrame:
        pass
