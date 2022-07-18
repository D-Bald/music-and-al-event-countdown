import functools
from datetime import datetime
import utils

# Following the recipe from https://realpython.com/primer-on-python-decorators/#both-please-but-never-mind-the-bread
def async_repeatable(jobs_dict={}, time=datetime.now().time().strftime("%H:%M:00")):
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
            utils.remove_task(guild_channel, jobs_dict)
            # Schedule new job
            utils.schedule_task(guild_channel, decorator(func), time, jobs_dict)
              
            return value
        return wrapper    
    return decorator
    