from datetime import date, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import operator

from db import db
from elo_system import EloSystem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
TODO:
- pull from memory instead of db?
- perhaps pymongo is already doing this?
"""


def _get_recent_games(elo_df):
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    tomorrow = str(date.today() + timedelta(days=1))
    acceptable_dates = [yesterday, today, tomorrow]

    for index, game in elo_df.copy().items():
        game_date = game["Date"].strftime("%Y-%m-%d")
        if game_date not in acceptable_dates:
            del elo_df[index]

    return elo_df


@app.get("/")
async def root():
    return {"message": "NHL ELO API"}


@app.get("/elotable")
def elo_table():
    elo_df = db.elo_table.find_one({"date_generated": str(date.today())})

    if elo_df is None:
        elo_df = EloSystem.process_elo_df().to_dict(orient="index")
        elo_df = _get_recent_games(elo_df)
        elo_df["date_generated"] = str(date.today())
        db.elo_table.insert_one(elo_df)

    elo_df["id"] = str(elo_df.pop("_id"))  # pydantic needs this line

    return elo_df


@app.get("/teamelos")
def team_elos():
    team_elo_dict = db.team_elos.find_one({"date_generated": str(date.today())})

    if team_elo_dict is None:
        team_elo_dict = EloSystem.get_elo_dict()
        team_elo_dict = dict(
            sorted(team_elo_dict.items(), key=operator.itemgetter(1), reverse=True)
        )
        team_elo_dict["date_generated"] = str(date.today())
        db.team_elos.insert_one(team_elo_dict)

    team_elo_dict["id"] = str(team_elo_dict.pop("_id"))  # pydantic needs this line

    return team_elo_dict


@app.put("/analytics")
def analytics():
    # EXPIREMENTAL: track things like page visits
    pass
