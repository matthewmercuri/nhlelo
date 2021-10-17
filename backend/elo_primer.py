import pandas as pd

from data import get_current_teams_list

"""
If change in ELO methodology, rerun the prev_season script to get updated
elo caclulations
"""


def get_previous_year_elo_df(previous_year):
    if previous_year == "20202021":
        starting_elo_df = pd.read_csv("backend/old_data/20202021seasonELOWITHADJ.csv")
        starting_elo_df.rename(
            columns={starting_elo_df.columns[0]: "team"}, inplace=True
        )

    return starting_elo_df


def get_starting_elo_dict(previous_year="20202021"):
    if previous_year != "20202021":
        raise KeyError(f"{previous_year} has not been implemented yet")

    current_teams_list = get_current_teams_list()
    starting_elo_df = get_previous_year_elo_df(previous_year)

    starting_team_elo_dict = {}
    for team in current_teams_list:
        if team == "Montréal Canadiens":
            _team = "Montreal Canadiens"
        else:
            _team = team

        try:
            team_entry = starting_elo_df[starting_elo_df["team"] == _team]
            team_start_elo = team_entry["New_ELO"].values.tolist()[0]
        except IndexError:
            # may be incorrect for other years (start at mean of prev elos?)
            team_start_elo = 1500

        starting_team_elo_dict[team] = team_start_elo

    return starting_team_elo_dict