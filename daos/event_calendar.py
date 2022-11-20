import pandas as pd
from datetime import datetime, date
from table2ascii import table2ascii as t2a, PresetStyle
from utils import datetime_tools
from config import EVENTS_FILEPATH


class WriteDaysLeftError(Exception):
    pass


class Event:
    def __init__(self, kuerzel: str, titel: str, start_datum: date, end_datum: date):
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

    def is_running(self):
        return datetime_tools.is_in_range(datetime.today(), self.start_datum, self.end_datum)

    def is_upcoming(self):
        return not datetime_tools.is_in_range(self.end_datum, self.start_datum, datetime.today())

class EventCalendar():
    async def upcoming_events(self) -> list[Event]:
        """
        Lists all event dates.

        Returns:
            List of `Event` objects.
        """
        df = pd.read_csv(EVENTS_FILEPATH,
                        parse_dates=['start_datum', 'end_datum'],
                        date_parser=datetime_tools.string_to_datetime)
        

        df["days_left"] = df["start_datum"].apply(datetime_tools.days_until)
        df = df.sort_values(by=["days_left"]).reset_index(drop=True)

        events = [
            Event(row["kuerzel"], row["titel"], row["start_datum"],
                row["end_datum"]) for _, row in df.iterrows()
        ]

        upcoming_events = list(filter(lambda event: (event.is_upcoming() or event.is_running()), events))

        return upcoming_events


    async def get_next_event(self) -> Event:
        """
        Filters out the next event.

        Returns:
            Next upcoming event.
        """
        event_list = await self.upcoming_events()
        event = event_list[0]

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
        output string with markdown table containing titel, start_datum and status.
    """
    body = [[
        event.titel, event.start_datum.date(), event.end_datum.date(),
        status(event)
    ] for event in list_of_events]

    output = t2a(header=["Name", "Start", "Ende", "Verbleibende Tage"],
                 body=body,
                 style=PresetStyle.thin_compact)

    return output


def status(event: Event) -> str|int:
    """
    Evaluates if the status is running and if not, how many days are left.

    Args:
        event: `Event` object

    Returns:
        `days_left` as int or "Die Veranstaltung läuft aktuell!" if event is currently running
        or "Die Veranstaltung ist bereits vorüber" if the event is in the past.
    """
    if event.is_running():
        return "Die Veranstaltung läuft aktuell!"
    elif event.is_upcoming():
        return event.days_left
    else:
        return "Die Veranstaltung ist bereits vorüber."
