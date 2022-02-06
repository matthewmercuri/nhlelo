from datetime import date, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import db
from app.data import Data
from app.utils import get_close_games

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


@app.get("/eloschedule")
def elo_table(window: str = "today"):
    if window not in ["today", "tomorrow", "close"]:
        raise TypeError(f"Invalid window argument ({window}).")

    elo_df = db.elo_table.find_one({"date_generated": str(date.today())})

    if elo_df is None:
        print("Calculating elos (cache invalid) -- /eloschedule")
        DataGrabber = Data()
        elo_df = DataGrabber.process_schedule_df().to_dict(orient="index")
        elo_df["date_generated"] = str(date.today())
        db.elo_table.insert_one(elo_df)
    else:
        print("Returning cached result -- /eloschedule")

    elo_df["id"] = str(elo_df.pop("_id"))  # pydantic needs this line
    date_generated = elo_df.pop("date_generated")
    id = elo_df.pop("id")

    data = [game for _, game in elo_df.items()]

    if window == "today":
        data = get_close_games(data, "today")
    elif window == "tomorrow":
        data = get_close_games(data, "tomorrow")
    elif window == "close":
        data = get_close_games(data, "close")

    response = {
        "data": data,
        "meta": {"date_generated": date_generated, "id": id},
    }

    return response


@app.get("/teamelotable")
def team_elos():
    team_elo_dict = db.team_elos.find_one({"date_generated": str(date.today())})

    if team_elo_dict is None:
        print("Calculating elos (cache invalid) -- /teamelotable")
        DataGrabber = Data()
        team_elo_dict = DataGrabber.get_team_elos().to_dict()[0]
        team_elo_dict["date_generated"] = str(date.today())
        db.team_elos.insert_one(team_elo_dict)
    else:
        print("Returning cached result -- /teamelotable")

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
