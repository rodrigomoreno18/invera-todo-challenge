from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz


def parse_datetime(datetime_str: str) -> datetime:
    return parse(datetime_str)


def utc_datetime(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0
) -> datetime:
    return datetime(year, month, day, hour, minute, second).replace(tzinfo=gettz("UTC"))
