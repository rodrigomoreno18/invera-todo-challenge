from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz


def naive_to_utc(naive: datetime) -> datetime:
    return naive.replace(tzinfo=gettz("UTC"))


def parse_utc_datetime(datetime_str: str) -> datetime:
    return naive_to_utc(parse(datetime_str))


def utc_datetime(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:
    return naive_to_utc(datetime(year, month, day, hour, minute, second))
