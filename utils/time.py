from datetime import datetime
from dateutil.parser import parse


def parse_datetime(datetime_str: str) -> datetime:
    return parse(datetime_str)