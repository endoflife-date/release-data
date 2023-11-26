from datetime import datetime, timezone
import calendar


def parse_date(text, formats=frozenset([
    "%B %d %Y",   # January 1 2020
    "%b %d %Y",   # Jan 1 2020
    "%d %B %Y",   # 1 January 2020
    "%d %b %Y",   # 1 Jan 2020
    "%d-%b-%Y",   # 1-Jan-2020
    "%d-%B-%Y",   # 1-January-2020
])) -> datetime:
    """Parse a given text representing a date using a list of formats.
    """
    return parse_datetime(text, formats, to_utc=False)


def parse_month_year_date(text, formats=frozenset([
    "%B %Y",      # January 2020
    "%b %Y",      # Jan 2020
    ])) -> datetime:
    """Parse a given text representing a partial date using a list of formats,
    adjusting it to the last day of the month.
    """
    date = parse_datetime(text, formats, to_utc=False)
    _, last_day = calendar.monthrange(date.year, date.month)
    return date.replace(day=last_day)


def parse_datetime(text, formats=frozenset([
    "%Y-%m-%d %H:%M:%S",         # 2023-05-01 08:32:34
    "%Y-%m-%dT%H:%M:%S",         # 2023-05-01T08:32:34
    "%Y-%m-%d %H:%M:%S %z",      # 2023-05-01 08:32:34 +0900
    "%a %d %b %Y %H:%M:%S %Z",  # Wed, 01 Jan 2020 00:00:00 GMT
    "%Y-%m-%dT%H:%M:%S%z",       # 2023-05-01T08:32:34+0900
]), to_utc=True) -> datetime:
    """Parse a given text representing a datetime using a list of formats,
    optionally converting it to UTC.
    """
    text = text.strip()
    text = text.replace(", ", " ")  # so that we don't have to deal with commas in formats
    for fmt in formats:
        try:
            date = datetime.strptime(text, fmt)
            date = date.astimezone(timezone.utc) if to_utc else date
            return date
        except ValueError:
            pass

    raise ValueError(f"'{text}' could not be parsed as a date with any of the formats: {str(formats)}")
