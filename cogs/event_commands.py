import disnake
from disnake.ext import commands

from repos import event_calendar


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
        events = await event_calendar.list_events()
        output = event_calendar.make_output_table(events)
        await inter.send(f"```{output}```")

    @commands.slash_command()
    async def next(self, inter: disnake.ApplicationCommandInteraction):
        """
        Sends back details about the next planned event.
    
        Args:
            ctx: discord.py context.
        """
        event = await event_calendar.get_next_event()
        embed = make_event_embed(event)

        await inter.send(embed=embed)


def make_event_embed(event):
    """
    Creates a discord embed for the given event.

    Args:
        event: event object
    Returns:
        discord.py embed
    """
    join = disnake.Embed(description='__%s__' % (event.titel),
                         title='Nächste Veranstaltung',
                         colour=0xFFFF)
    # join.set_thumbnail(url = WEBSCRAPER_ERGEBNIS)
    # join.add_field(name = '__Titel__', value = event["titel"])
    join.add_field(name='Start', value=event.start_datum)
    join.add_field(name='Ende', value=event.end_datum)
    join.add_field(name='Link', value=event.link)

    # join.set_footer(text ='Created: %s'%time)

    return join


def setup(bot: commands.Bot):
    bot.add_cog(EventCommands(bot))
