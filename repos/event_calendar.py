import pandas as pd
from table2ascii import table2ascii as t2a, PresetStyle
from utils import datetime_tools

FILEPATH = './data/dates.csv'


class WriteDaysLeftError(Exception):
    pass


class Event:
    def __init__(self, kuerzel, titel, start_datum, end_datum):
        self.kuerzel = kuerzel
        self.titel = titel
        self.start_datum = start_datum
        self.end_datum = end_datum
        self.link = 'https://www.music-and-al.de/veranstaltungen/' + kuerzel

    def __repr__(self):
        repr = f"Kuerzel: {self.kuerzel}, Titel: {self.titel}, Start: {self.start_datum}, Ende: {self.end_datum}, Link: {self.link}"
        return repr

    @property
    def days_left(self):
        """Number of days until the birthdays."""
        return datetime_tools.days_until(self.start_datum)

    @days_left.setter
    def days_left(self, _value):
        return WriteDaysLeftError("days left is a computed attribute")


async def list_events():
    """
    Lists all event dates.

    Returns:
        List of `Event` objects.
    """
    df = pd.read_csv(FILEPATH)

    df["days_left"] = df["start_datum"].apply(datetime_tools.days_until)
    df = df.sort_values(by=["days_left"]).reset_index(drop=True)

    events = [
        Event(row["kuerzel"], row["titel"], row["start_datum"],
              row["end_datum"]) for _, row in df.iterrows()
    ]

    return events


async def get_next_event():
    """
    Filters out the next event.

    Returns:
        Next upcoming event.
    """
    event_list = await list_events()
    event = event_list[
        0]  # TODO: change this line to actually filter the next event from a list where some events might be in the past. Return running event if todays date lays between a start and end date.

    ## DEBUGGING ##
    from pprint import pprint
    pprint(event)
    ###############

    return event


#################################################
# Output styling for events
#################################################


def make_output_table(list_of_events):
    """
    Builds a markdown table as code-block from given list of `Event` objects.

    Args:
        list_of_birthdays: list of `Event` objects

    Returns:
        output string with markdown table containing titel, start_datum and days_left or "HEUTE GEHT ES LOS!" if days_left is equal to zero.
    """
    body = [[
        bd.titel, bd.start_datum, bd.end_datum,
        _exclamation_if_zero_days_left(bd.days_left)
    ] for bd in list_of_events]

    output = t2a(header=["Name", "Start", "Ende", "Verbleibende Tage"],
                 body=body,
                 style=PresetStyle.thin_compact)

    return output


def _exclamation_if_zero_days_left(days_left):
    # TODO: Change to also check start and end date and show a message if the event is running at the Moment
    if days_left == 0:
        return "HEUTE GEHT ES LOS!"
    else:
        return days_left
