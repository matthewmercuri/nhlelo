import datetime
import numpy as np
import pandas as pd

from elo import update_elo

STARTING_ELO = 1500

"""
This script processes last season's data to create a new pandas dataframe
that holds the starting elos for the current season.

Should the ELO methodology be changed in elo.py, the script must be run
to generate a new '{season}seasonELOWITHADJ.csv' file that informs the
starting elos to use in the current season.
"""

df = pd.read_csv("backend/old_data/20202021season.csv", index_col=0)
rename_dict = {"Visitor": "Away", "G": "Away_Goals", "G.1": "Home_Goals"}
df.rename(columns=rename_dict, inplace=True)
df.drop(columns=df.columns[-4:], inplace=True)
df["MOV"] = np.absolute(df["Away_Goals"] - df["Home_Goals"])
df[["Away_B2B", "Home_B2B"]] = 0
df[["Away_ELO", "Home_ELO"]] = STARTING_ELO
df.index = pd.to_datetime(df.index)

teams = set(df["Away"].tolist())
_starting_elo_list = [STARTING_ELO] * len(teams)
teams_elo_dict = dict(zip(teams, _starting_elo_list))


def _back_to_back(row):
    game_date = row.name
    prev_day = game_date - datetime.timedelta(1)
    away_team = row["Away"]
    home_team = row["Home"]

    prev_date_df = df[df.index == prev_day]

    prev_date_away_teams = prev_date_df["Away"].tolist()
    prev_date_home_teams = prev_date_df["Home"].tolist()
    prev_date_teams = prev_date_away_teams + prev_date_home_teams

    if away_team in prev_date_teams:
        row["Away_B2B"] = 1
    if home_team in prev_date_teams:
        row["Home_B2B"] = 1

    return row


def _apply_elo(row):
    if row["Away_Goals"] > row["Home_Goals"]:
        away_win = 1
    else:
        away_win = 0

    away_team_elo, home_team_elo = update_elo(
        teams_elo_dict[row["Away"]],
        teams_elo_dict[row["Home"]],
        row["Away_B2B"],
        row["Home_B2B"],
        away_win,
    )

    teams_elo_dict[row["Away"]] = away_team_elo
    teams_elo_dict[row["Home"]] = home_team_elo
    row["Away_ELO"] = away_team_elo
    row["Home_ELO"] = home_team_elo

    return row


df = df.apply(_back_to_back, axis=1)
df = df.apply(_apply_elo, axis=1)

elo_df = pd.DataFrame.from_dict(teams_elo_dict, orient="index")
elo_df = elo_df.sort_values(by=[elo_df.columns[0]], ascending=False)

elo_mean = elo_df[0].mean()
elo_std = elo_df[0].std()

elo_df["Z_Score"] = 0
elo_df["Z_Score"] = elo_df.apply(lambda x: (x[0] - elo_mean) / elo_std, axis=1)
elo_df["Side_of_Mean"] = elo_df["Z_Score"].apply(lambda x: -1 if x < 0 else 1)
elo_df["Log_of_Z_plus_One"] = elo_df["Z_Score"].apply(
    lambda x: np.log(np.absolute(x) + 1)
)
elo_df["New_ELO"] = elo_df.apply(
    lambda x: elo_mean + (x["Log_of_Z_plus_One"] * elo_std * x["Side_of_Mean"]),
    axis=1,
)

elo_df.to_csv("backend/old_data/20202021seasonELOWITHADJ.csv")
