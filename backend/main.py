from fastapi import FastAPI
import operator

from elo_system import EloSystem

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "NHL ELO API"}


@app.get("/elotable")
def elo_table():
    elo_df = EloSystem.process_elo_df()
    return elo_df.to_dict(orient="index")


@app.get("/teamelos")
def team_elos():
    # return the elo of all teams
    team_elo_dict = EloSystem.get_elo_dict()
    team_elo_dict = dict(
        sorted(team_elo_dict.items(), key=operator.itemgetter(1), reverse=True)
    )
    return team_elo_dict


@app.put("/analytics")
def analytics():
    # EXPIREMENTAL: track things like page visits
    pass
