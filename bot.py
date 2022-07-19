import asyncio
import os
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import async_scheduling
import event_calendar
import utils
import subscriptions
from config import PREFIX, PUBLISH_COUNTDOWN_TIME

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)

# Dictionary to store the jobs per channel id to be able to unsubscribe and therefore cancel the job for the unsubscribing channel
scheduled_subscription_jobs = {}


@bot.command()
async def events(ctx):
    """
    Sends back a list of the next planned events.

    Args:
        ctx: discord.py context.
    """
    events = await event_calendar.get_all_events()
    output = utils.make_output_table(events)
    await ctx.send(f"```{output}```")


@bot.command()
async def next(ctx):
    """
    Sends back details about the next planned event.

    Args:
        ctx: discord.py context.
    """
    event = await event_calendar.get_next_event()
    embed = _make_event_embed(event)

    await ctx.send(embed = embed)

def _make_event_embed(event):
    """
    Creates a discord embed for the given event.

    Args:
        event: event (currently as pandas dataframe)
    Returns:
        discord.py embed
    """
    join = discord.Embed(description= '__%s__'%(event["title"]),title = 'Nächste Veranstaltung', colour = 0xFFFF)
    # join.set_thumbnail(url = WEBSCRAPER_ERGEBNIS)
    # join.add_field(name = '__Titel__', value = event["title"])
    join.add_field(name = 'Start', value = event["start_date"])
    join.add_field(name = 'Ende', value = event["end_date"])
    join.add_field(name = 'Link', value = 'https://www.music-and-al.de/veranstaltungen/' + event["event"])

    # join.set_footer(text ='Created: %s'%time)

    return join

@bot.command()
async def subscribe(ctx):
    """
    Schedules a job to be executed at PUBLISH_COUNTDOWN_TIME from config.py.

    Args:
        ctx: discord.py context.
    """

    # Only add new subscription if guild is not subscribed yet
    if ctx.channel.id not in scheduled_subscription_jobs:
        await _subscribe_channel(ctx.channel)

        await ctx.send(f"Subscription successful.")
    else:
        await ctx.send(f"Already subscribed.")

async def _subscribe_channel(channel):
    """
    Schedules a job to be executed at PUBLISH_BIRTHDAYS_TIME from config.py.

    Args:
        channel_id: discord.py channel
    """
    async_scheduling.new_task(channel, publish_daily_countdown, PUBLISH_COUNTDOWN_TIME, scheduled_subscription_jobs)

@bot.command()
async def unsubscribe(ctx):
    """
    Removes a job associated with the guild_id derived from the context from the global dictionary `scheduled_subscription_jobs`
    and cancel the job from the scheduler.

    Args:
        ctx: discord.py context.
    """
    async_scheduling.remove_task(ctx.channel, scheduled_subscription_jobs)

    await ctx.send(f"Successfully unsubsribed.")

@async_scheduling.repeatable_decorator(jobs_dict=scheduled_subscription_jobs, time=PUBLISH_COUNTDOWN_TIME)
async def publish_daily_countdown(guild_channel):
    """
    Fetches the list of events and publishes it to the given context.

    On subscription a task is created and scheduled to execute this coroutine with the correct context
    (e.g. to send the message to the channel, that the subscribe command was called in).

    Args:
        guild_channel: discord.py discord.abc.GuildChannel
    """
    event = await event_calendar.get_next_event()
    embed = _make_event_embed(event)

    await guild_channel.send(embed = embed)


@bot.event
async def on_ready():
    print("----------------------")
    print("Beigetreten als")
    print("Username: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("Zeit: %s"%datetime.now().time())
    print("----------------------")

    # Load saved subscriptions
    subs_list = subscriptions.load_subscribed_channels()
    channels = [await bot.fetch_channel(channel_id) for channel_id in subs_list]
    await asyncio.gather(*[_subscribe_channel(channel) for channel in channels])

    print("Scheduled subscription jobs")
    print(scheduled_subscription_jobs)
    print("----------------------")

    # Run periodically scheduled tasks
    bot.loop.create_task(async_scheduling.run_scheduled_jobs(sleep=1))


if __name__ == "__main__":
    bot.run(TOKEN)

