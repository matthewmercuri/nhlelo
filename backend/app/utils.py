from datetime import datetime, timedelta, tzinfo
from zoneinfo import ZoneInfo
from pytz import timezone


def get_close_games(schedule, window):
    """
    close is games from today and tomorrow
    """

    todays_schedule = []
    tomorrows_schedule = []
    todays_date = datetime.now(timezone("US/Eastern"))
    todays_date_string = todays_date.strftime("%Y-%m-%d")
    tomorrows_date_string = (todays_date + timedelta(1)).strftime("%Y-%m-%d")

    if window == "today" or window == "close":
        for game in schedule:
            if todays_date_string == game["dateEst"]:
                todays_schedule.append(game)

    if window == "tomorrow" or window == "close":
        for game in schedule:
            if tomorrows_date_string == game["dateEst"]:
                tomorrows_schedule.append(game)

    return todays_schedule, tomorrows_schedule
