import numpy as np
import pandas as pd

from prev_season import get_elo_df

df = pd.read_csv("backend/old_data/20202021seasonPROCESSED.csv", index_col=0)
# df = pd.read_csv("backend/old_data/20202021season.csv", index_col=0)
# df = pd.read_csv("backend/old_data/20192020season.csv", index_col=0)
# df = pd.read_csv("backend/old_data/20182019season.csv", index_col=0)

rename_dict = {"Visitor": "Away", "G": "Away_Goals", "G.1": "Home_Goals"}
df.rename(columns=rename_dict, inplace=True)


def _home_win(row):
    if row["Away_Goals"] < row["Home_Goals"]:
        return 1
    else:
        return 0


def find_home_ice_advantage():
    """
    Home ice advantage
    - COVID: 3.33
    - 20192020: 3.33
    - 20182019: 3.66
    """
    df["Is_Home_Win"] = df.apply(_home_win, axis=1)

    home_wins = df["Is_Home_Win"].sum()
    total_games = len(df)

    home_win_percent = round((home_wins / total_games) * 100, 2)

    print(f"The home team won {home_win_percent}% of games")


def _b2b_win(row):
    if row["Away_Goals"] < row["Home_Goals"]:
        if row["Home_B2B"] == 1:
            return 1
        else:
            return 0
    else:
        if row["Away_B2B"] == 1:
            return 1
        else:
            return 0


def _one_team_b2b(row):
    if (row["Home_B2B"] == 1) ^ (row["Away_B2B"] == 1):
        return 1
    else:
        return 0


def back_to_back_disadvantage():
    """
    20202021 season: ~14 percent disadvantage of being on a b2b vs. fresh opp
    """
    df["One_Team_B2B"] = df.apply(_one_team_b2b, axis=1)
    new_df = df[df["One_Team_B2B"] == 1]
    new_df["Is_B2B_Win"] = new_df.apply(_b2b_win, axis=1)

    b2b_wins = new_df["Is_B2B_Win"].sum()
    total_games = len(new_df)

    b2b_win_percent = round((b2b_wins / total_games) * 100, 2)
    print(new_df)

    print(f"A back to back team won {b2b_win_percent}% of games")


# def elo_adj():
#     elo_df = get_elo_df()
#     elo_mean = elo_df[0].mean()
#     elo_std = elo_df[0].std()

#     elo_df["Z_Score"] = elo_df.apply(lambda x: (x - elo_mean) / elo_std, axis=1)

#     print(elo_df)


# find_home_ice_advantage()
# back_to_back_disadvantage()
# elo_adj()
