from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_close_games(schedule, window):
    """
    close is games from today and tomorrow
    """

    todays_schedule = []
    todays_date = datetime.utcnow().replace(tzinfo=ZoneInfo("America/New_York"))
    todays_date_string = todays_date.strftime("%Y-%m-%d")
    tomorrows_date_string = (todays_date + timedelta(1)).strftime("%Y-%m-%d")

    if window == "today":
        for game in schedule:
            if todays_date_string == game["dateEst"]:
                todays_schedule.append(game)

    if window == "tomorrow":
        for game in schedule:
            if tomorrows_date_string == game["dateEst"]:
                todays_schedule.append(game)

    if window == "close":
        for game in schedule:
            if game["dateEst"] in [
                todays_date_string,
                tomorrows_date_string,
            ]:
                todays_schedule.append(game)

    return todays_schedule
