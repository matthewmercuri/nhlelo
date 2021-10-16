import pandas as pd

df = pd.read_csv("backend/old_data/20202021season.csv", index_col=0)
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


find_home_ice_advantage()
