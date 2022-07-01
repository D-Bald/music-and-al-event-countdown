import os
import asyncio
import schedule
import discord
from pprint import pprint
from discord.ext import commands
from dotenv import load_dotenv
from config import PREFIX, PUBLISH_COUNTDOWN_TIME
import event_calendar
import utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=PREFIX)

# Dictionary to store the jobs per guild to be able to unsubscribe and therefore cancel the job for the unsubscribing guild
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
    join = discord.Embed(description= '__%s__'%(event["title"]),title = 'Nächste Veranstaltung', colour = 0xFFFF)
    # join.set_thumbnail(url = WEBSCRAPER_ERGEBNIS)
    # join.add_field(name = '__Titel__', value = event["title"])
    join.add_field(name = 'Start', value = event["start_date"])
    join.add_field(name = 'Ende', value = event["end_date"])
    join.add_field(name = 'Link', value = 'https://www.music-and-al.de/veranstaltungen/' + event["event"])

    # join.set_footer(text ='Created: %s'%time)

    await ctx.send(embed = join)


@bot.command()
async def subscribe(ctx):
    """
    Schedules a job to be executed at PUBLISH_COUNTDOWN_TIME from config.py and stores guild_id and job-instance
    as key-value pair in a global dictionary `scheduled_subscription_jobs` for later cancelation.

    Args:
        ctx: discord.py context.
    """

    # Only add new subscription if guild is not subscribed yet
    if ctx.guild.id not in scheduled_subscription_jobs:
        job = schedule.every().day.at(PUBLISH_COUNTDOWN_TIME).do(asyncio.create_task, publish_daylie_countdown(ctx))
        scheduled_subscription_jobs[ctx.guild.id] = job

        print("----------------------")
        print("Current jobs (guild_id: job_details):\n")
        pprint(scheduled_subscription_jobs)
        print("----------------------")

        await ctx.send(f"Subscription successful.")
    else:
        await ctx.send(f"Already subscribed.")


@bot.command()
async def unsubscribe(ctx):
    """
    Removes a job associated with the guild_id derived from the context from the global dictionary `scheduled_subscription_jobs`
    and cancel the job from the scheduler.

    Args:
        ctx: discord.py context.
    """
    job = scheduled_subscription_jobs.pop(ctx.guild.id)
    schedule.cancel_job(job)

    print("----------------------")
    print("Current jobs (guild_id: job_details):\n")
    pprint(scheduled_subscription_jobs)
    print("----------------------")

    await ctx.send(f"Successfully unsubsribed.")


async def publish_daylie_countdown(ctx):
    """
    Fetches the list of events and publishes it to the given context.

    On subscription a task is created and scheduled to execute this coroutine with the correct context
    (e.g. to send the message to the channel, that the subscribe command was called in).

    Args:
        ctx: discord.py context.
    """

    events = await event_calendar.get_all_events()
    output = utils.make_output_table(events)

    await ctx.send(f"```{output}```")

    # Reschedule the job due to exception=RuntimeError('cannot reuse already awaited coroutine')
    # (ugly bug fix)
    job_old = scheduled_subscription_jobs.pop(ctx.guild.id)
    schedule.cancel_job(job_old)
    job_new = schedule.every().day.at(PUBLISH_COUNTDOWN_TIME).do(asyncio.create_task, publish_daylie_countdown(ctx))
    scheduled_subscription_jobs[ctx.guild.id] = job_new


async def run_scheduled_jobs(sleep=1):
    """
    Loop to run jobs as soon as the scheduler marks them as pending.
    
    This is executed as task in the handler for the 'on_ready' bot event.

    Args:
        sleep: number of seconds to wait between retries to run pending jobs.
    """
    while True:
        schedule.run_pending()
        await asyncio.sleep(sleep)


@bot.event
async def on_ready():
    print("----------------------")
    print("Beigetreten als")
    print("Username: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("----------------------")

    # Run periodically scheduled tasks
    bot.loop.create_task(run_scheduled_jobs(sleep=1))


bot.run(TOKEN)
