import calendar
from datetime import datetime, timezone


def parse_date(text: str, formats: list[str] = frozenset([
    "%B %d %Y",  # January 1 2020
    "%b %d %Y",  # Jan 1 2020
    "%d %B %Y",  # 1 January 2020
    "%d %b %Y",  # 1 Jan 2020
    "%d-%b-%Y",  # 1-Jan-2020
    "%d-%B-%Y",  # 1-January-2020
    "%Y-%m-%d",  # 2020-01-01
    "%m/%d/%Y",  # 01/25/2020
])) -> datetime:
    """Parse a given text representing a date using a list of formats.
    """
    return parse_datetime(text, formats, to_utc=False)


def parse_month_year_date(text: str, formats: list[str] = frozenset([
    "%B %Y",  # January 2020
    "%b %Y",  # Jan 2020
])) -> datetime:
    """Parse a given text representing a partial date using a list of formats,
    adjusting it to the last day of the month.
    """
    date = parse_datetime(text, formats, to_utc=False)
    _, last_day = calendar.monthrange(date.year, date.month)
    return date.replace(day=last_day)


def parse_datetime(text: str, formats: list[str] = frozenset([
    "%Y-%m-%d %H:%M:%S",         # 2023-05-01 08:32:34
    "%Y-%m-%dT%H:%M:%S",         # 2023-05-01T08:32:34
    "%Y-%m-%d %H:%M:%S %z",      # 2023-05-01 08:32:34 +0900
    "%Y-%m-%dT%H:%M:%S%z",       # 2023-05-01T08:32:34+0900
    "%Y-%m-%dT%H:%M:%S.%f%z",    # 2023-05-01T08:32:34.123456Z
    "%a %d %b %Y %H:%M:%S %Z",   # Wed, 01 Jan 2020 00:00:00 GMT
]), to_utc: bool = True) -> datetime:
    """Parse a given text representing a datetime using a list of formats,
    optionally converting it to UTC.
    """
    # so that we don't have to deal with some special characters in formats
    text = text.strip().replace(", ", " ").replace(". ", " ").replace("(", "").replace(")", "")
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)  # NOQA: DTZ007, timezone is handled below

            if to_utc:
                dt = dt.astimezone(timezone.utc)
            elif dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            return dt
        except ValueError:
            pass

    msg = f"'{text}' could not be parsed as a date with any of the formats: {str(formats)}"
    raise ValueError(msg)


def date(year: int, month: int, day: int) -> datetime:
    """Create a datetime object with the given year, month and day, at midnight."""
    return datetime(year, month, day, tzinfo=timezone.utc)


def today() -> datetime:
    """Create a datetime object with today's date, at midnight."""
    return datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
