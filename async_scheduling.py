import asyncio
import functools
import schedule
from datetime import datetime
import subscriptions

# Following the recipe from https://realpython.com/primer-on-python-decorators/#both-please-but-never-mind-the-bread
def repeatable_decorator(jobs_dict={}, time=datetime.now().time().strftime("%H:%M:00")):
    """
    Removes and reschedules a function using the scheduler package.

    This is an ugly bugfix to work around the exception:
        RuntimeError('cannot reuse already awaited coroutine')
    
    Args:
        jobs_dict: dictionary containing all scheduled jobs associated to the guild_id
        time: time to that the function should be rescheduled. Defaults to the current time when decorator is invoked.

    Returns:
        A decorator function that expects the wrapped function to pass a discord.py GuildChannel as first positional argument.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(guild_channel, *args, **kwargs):
            value = await func(guild_channel, *args, **kwargs)
            # Remove and cancel old job
            remove_task(guild_channel, jobs_dict)
            # Schedule new job
            new_task(guild_channel, decorator(func), time, jobs_dict)
              
            return value
        return wrapper    
    return decorator
    
def new_task(guild_channel, func, time, jobs_dict):
    """
    Schedules new job for the given func that is executed with ctx as parameter at the given time.
    
    Stores channel_id and job-instance as key-value pair in a global dictionary `scheduled_subscription_jobs` for later cancelation.
    Prints out the resulting list of current scheduled jobs.
    The func is scheduled as asynchronous task so it has to be awaited or run as task itself!

    Args:
        guild_channel: discord.py discord.abc.GuildChannel
        func: the function that is run with ctx as parameter
        time: time in string format that the scheduler uses to schedule the task
        jobs_dict: dictionary containing all scheduled jobs associated to the channel_id
    """
    job = schedule.every().day.at(time).do(asyncio.create_task, func(guild_channel))
    # job = schedule.every(10).seconds.do(asyncio.create_task, func(guild_channel)) # uncomment for debugging

    jobs_dict[guild_channel.id] = job

    subscriptions.save_subscribed_channels(guild_channel)

    # print("----------------------")
    # print("Current jobs (channel_id: job_details):\n")
    # pprint(jobs_dict)
    # print("----------------------")


def remove_task(guild_channel, jobs_dict):
    """
    Removes the task associated to the given context in the dictionary and cancels it from scheduler.

    Prints out the resulting list of current scheduled jobs.

    Args:
        guild_channel: discord.py discord.abc.GuildChannel
        jobs_dict: dictionary containing all scheduled jobs associated to the channel_id
    """
    job = jobs_dict.pop(guild_channel.id)
    schedule.cancel_job(job)

    subscriptions.delete_subscribed_channel(guild_channel)

    # print("----------------------")
    # print("Current jobs (channel_id: job_details):\n")
    # pprint(jobs_dict)
    # print("----------------------")


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