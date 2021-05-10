import datetime

import pytz


def naive_to_local(dt: datetime.datetime, timezone='Europe/Moscow'):
    tz = pytz.timezone(timezone)
    loc_dt = tz.localize(dt)
    return loc_dt


def utc_to_local(dt: datetime.datetime, timezone='Europe/Moscow'):
    tz = pytz.timezone(timezone)
    loc_dt = dt.astimezone(tz)
    return loc_dt


def local_to_utc(dt: datetime.datetime):
    return dt.astimezone(pytz.UTC)


def get_local_now(timezone='Europe/Moscow'):
    tz = pytz.timezone(timezone)
    return datetime.datetime.now(pytz.UTC).astimezone(tz)
