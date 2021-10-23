from fastapi import FastAPI

from elo_system import EloSystem

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "NHL ELO API"}


@app.get("/elotable")
def elo_table():
    elo_df = EloSystem.process_elo_df()
    return elo_df.to_json(orient="table")
