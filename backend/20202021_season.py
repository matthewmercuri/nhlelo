import datetime
import numpy as np
import pandas as pd

STARTING_ELO = 1500

df = pd.read_csv("backend/old_data/20202021season.csv", index_col=0)
rename_dict = {"Visitor": "Away", "G": "Away_Goals", "G.1": "Home_Goals"}
df.rename(columns=rename_dict, inplace=True)
df.drop(columns=df.columns[-4:], inplace=True)
df["MOV"] = np.absolute(df["Away_Goals"] - df["Home_Goals"])
df[["Away_B2B", "Home_B2B"]] = 0
df[["Away_ELO", "Home_ELO"]] = STARTING_ELO
df.index = pd.to_datetime(df.index)


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


df = df.apply(_back_to_back, axis=1)
df.to_csv("backend/old_data/20202021seasonPROCESSED.csv")
