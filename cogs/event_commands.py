import disnake
from disnake.ext import commands

from daos import event_calendar
import daos.event_calendar as ec
from utils.datetime_tools import format_date

class EventCommands(commands.Cog):
    """Handling interactions to get event infos."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def events(self, inter: disnake.ApplicationCommandInteraction):
        """Sends back a list of the all available events."""
        """
        Args:
            inter: disnake.ApplicationCommandInteraction object
        """
        events = await ec.EventCalendar().upcoming_events()

        output = ec.make_output_table(events)
        await inter.send(f"```{output}```")
    

    @commands.slash_command()
    async def next(self, inter: disnake.ApplicationCommandInteraction):
        """
        Sends back details about the next planned event.
    
        Args:
            ctx: discord.py context.
        """
        event = await ec.EventCalendar().get_next_event()
        embed = make_event_embed(event)

        await inter.send(embed=embed)


def make_event_embed(event: ec.Event):
    """
    Creates a discord embed for the given event.

    Args:
        event: event object
    Returns:
        discord.py embed
    """
    join = disnake.Embed(description=f'[{event.titel}]({event.link})',
                         title='Nächste Veranstaltung',
                         colour=0xFFFF)
    # join.set_thumbnail(url = WEBSCRAPER_ERGEBNIS)
    # join.add_field(name = '__Titel__', value = event["titel"])
    join.add_field(name='Start', value=format_date(event.start_datum))
    join.add_field(name='Ende', value=format_date(event.end_datum))
    join.add_field(name='Verbleibende Tage', value=event.days_left)

    # join.set_footer(text ='Created: %s'%time)

    return join


def setup(bot: commands.Bot):
    bot.add_cog(EventCommands(bot))
