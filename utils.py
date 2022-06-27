from datetime import datetime
import pandas as pd
from table2ascii import table2ascii as t2a, PresetStyle
from config import DATE_FORMAT

def make_output_table(df):
    """Builds a markdown table as code-block from given dataframe.

    Args:
        df: pandas DataFrame with columns `name`, `date` and `days_left`

    Returns:
        output string with markdown table containing name, date and days_left or "Herzlichen Glückwunsch" if days_left is equal to zero.
    """
    body = []
    for i in df.index:
        entry = [df["title"].iloc[i], df["start_date"].iloc[i], df["days_left"].apply(_exclamation_if_zero_days_left).iloc[i]]
        body.append(entry)

    output = t2a(
        header=["Titel", "Start Datum", "Verbleibende Tage"],
        body=body,
        style=PresetStyle.thin_compact
    )

    return output

def make_output_table_for_event(df: pd.DataFrame, event: str):
    # Suche den Eintrag für den gegebenen Namen
    event = df.iloc[df[df["event"] == event].index[0]]

    # Erstelle Tabelle
    output = t2a(
        header=["Titel", "Start Datum", "Verbleibende Tage"],
        body=[[event["title"], event["start_date"], _exclamation_if_zero_days_left(event["days_left"])]],
        style=PresetStyle.thin_compact
    )

    return output

def check_date_format(date: str):
    """Checks if the given date has the date format specified in config.py.

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
    """Parses a date string to datetime format.

    Args:
        date_str: the date as string with format as specified in config.py
    
    Returns:
        Datetime object with given date and time "00:00:00"
    """
    date = datetime.strptime(date_str, DATE_FORMAT)
    return date

def format_date_string(date_str: str):
    """parses a date string to string with format specified in config.py.

    Args:
        date_str: the date as string with format like `"%d.%m.%Y"`
    
    Returns:
        Given date as string in format specified in config.py
    """
    date = string_to_datetime(date_str)
    return datetime.strftime(date, DATE_FORMAT)

def _exclamation_if_zero_days_left(days_left):
    if days_left == 0:
        return "HEUTE GEHT ES LOS!"
    else:
        return days_left