from datetime import datetime


def get_todays_games(schedule):
    todays_schedule = []
    todays_date = datetime.today().strftime("%Y-%m-%d")

    for game in schedule:
        if todays_date == game["dateEst"]:
            todays_schedule.append(game)

    return todays_schedule
