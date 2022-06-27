import datetime
import pandas as pd
import utils

FILEPATH = './data/dates.csv'

async def get_all_events():
    """Gets all event dates.

    Returns:
        All events as pandas DataFrame with columns `event`, `title`, `start_date`, `end_date` and `dates_left`.
    """
    df = pd.read_csv(FILEPATH)

    df["days_left"] = df["start_date"].apply(days_left)
    df = df.sort_values(by=["days_left"]).reset_index(drop=True)
    return df

async def get_next_event():
    """Filters out the next event.

    Returns:
        Next upcoming event as pandas DataFrame with columns `event`, `title`, `start_date`, `end_date` and `dates_left`.
    """
    df = await get_all_events()
    df = df.iloc[0]
  
    return df

def days_left(date_str: str):
    """Calculates the number of days until the given date.

    Args:
        date_str: the date as string
    
    Returns:
        Days until the given date as integer.
    """
    # parse from string
    date = utils.string_to_datetime(date_str).date()
    today = datetime.datetime.today().date()

    return (date - today).days