from datetime import datetime, date
from config import DATE_FORMAT

def check_date_format(date: str):
    """
    Checks if the given date has the date format specified in config.py.

    Args:
        date: the date as string

    Returns:
        `True` if the date is in the correct format, `False` else.
    """
    res = True
    try:
        res = bool(datetime.strptime(date, DATE_FORMAT))
    except ValueError:
        res = False
    return res


def string_to_datetime(date_str: str):
    """
    Parses a date string to datetime format.

    Args:
        date_str: the date as string with format as specified in config.py
    
    Returns:
        Datetime object with given date and time "00:00:00"
    """
    date = datetime.strptime(date_str, DATE_FORMAT)
    return date


def format_date_string(date_str: str) -> str:
    """
    Parses a date string to string with format specified in config.py.

    Args:
        date_str: the date as string with format like `"%d.%m.%Y"`
    
    Returns:
        Given date as string in format specified in config.py
    """
    date = string_to_datetime(date_str)
    return datetime.strftime(date, DATE_FORMAT)


def format_date(date: datetime) -> str:
    """
    Parses a date string to string with format specified in config.py.

    Args:
        date: the date as datetime object
    
    Returns:
        Given date as string in format specified in config.py
    """
    return datetime.strftime(date, DATE_FORMAT)


def days_until(date: datetime|str) -> int:
    """
    Calculates the number of days until the given date.

    Args:
        date: the date as string or datetime object
    
    Returns:
        Days until the given date as integer. Returns negative number if the date is in the past.
    """

    if isinstance(date, str):
        # Parse from string
        date = string_to_datetime(date)

    today = datetime.today()
    
    return (date.date() - today.date()).days

def is_in_range(date: datetime, start_date: datetime, end_date: datetime) -> bool:
    """
    Checks if the given date is in a given range.
    """
    return start_date.date() < date.date() < end_date.date()