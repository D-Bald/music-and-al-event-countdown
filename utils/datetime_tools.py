from datetime import datetime
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


def format_date_string(date_str: str):
    """
    Parses a date string to string with format specified in config.py.

    Args:
        date_str: the date as string with format like `"%d.%m.%Y"`
    
    Returns:
        Given date as string in format specified in config.py
    """
    date = string_to_datetime(date_str)
    return datetime.strftime(date, DATE_FORMAT)

def days_until(date):
    """
    Calculates the number of days until the given date.

    Args:
        date: the date as string or datetime object
    
    Returns:
        Days until the given date as integer.
    """

    if isinstance(date, str):
        # Parse from string
        date = string_to_datetime(date)

    # Set year to current year
    today = datetime.today().date()
    date = datetime(today.year,date.month,date.day).date()

    # Check if birthday is this year or next year
    # Adjust year accordingly
    if (date - today).days < 0:
        date = datetime(today.year + 1,date.month,date.day).date()
    
    return (date - today).days

def has_birthday_today(date):
    """
    Checks if the given date matches todays month and day.

    Args:
        date_str: the date as string or datetime object
    
    Returns:
        `True` if the date indicates a birthday today; `False` else.
    """
    if isinstance(date, str):
        # Parse from string
        date = string_to_datetime(date)

    today = datetime.today()
    if (date.month == today.month) and (date.day == today.day):
        return True
    return False