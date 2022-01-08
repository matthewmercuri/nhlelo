from datetime import date, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import operator

from app.db import db
from app.data import Data

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


@app.get("/")
async def root():
    return {"message": "NHL ELO API"}


@app.get("/elotable")
def elo_table():
    elo_df = db.elo_table.find_one({"date_generated": str(date.today())})

    if elo_df is None:
        elo_df = Data.process_schedule_df().to_dict(orient="index")
        elo_df["date_generated"] = str(date.today())
        db.elo_table.insert_one(elo_df)

    elo_df["id"] = str(elo_df.pop("_id"))  # pydantic needs this line
    date_generated = elo_df.pop("date_generated")
    id = elo_df.pop("id")

    response = {
        "data": [game for _, game in elo_df.items()],
        "meta": {"date_generated": date_generated, "id": id},
    }

    return response


@app.get("/teamelos")
def team_elos():
    team_elo_dict = db.team_elos.find_one({"date_generated": str(date.today())})

    if team_elo_dict is None:
        team_elo_dict = Data.get_team_elos().to_dict(orient="index")
        team_elo_dict = dict(
            sorted(team_elo_dict.items(), key=operator.itemgetter(1), reverse=True)
        )
        team_elo_dict["date_generated"] = str(date.today())
        db.team_elos.insert_one(team_elo_dict)

    team_elo_dict["id"] = str(team_elo_dict.pop("_id"))  # pydantic needs this line
    date_generated = team_elo_dict.pop("date_generated")
    id = team_elo_dict.pop("id")

    response = {
        "data": [{team: elo} for team, elo in team_elo_dict.items()],
        "meta": {"date_generated": date_generated, "id": id},
    }

    return response


@app.put("/analytics")
def analytics():
    # EXPIREMENTAL: track things like page visits
    pass
