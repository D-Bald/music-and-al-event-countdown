import pandas as pd

FILEPATH = './data/subscriptions.csv'

def read_subscribed_channels():
    """
    Reads channel ids to be scheduled and returns them as list.

    Returns:
        List of ids of subscribed channels
    """
    df_subs = pd.read_csv(FILEPATH)
    subs_list = df_subs["channel_id"].values.tolist()
    return subs_list


def save_subscribed_channels(channel):
    """
    Saves the given channel to be scheduled again on start-up.

    Args:
        guild_channel: disnake.abc.GuildChannel
    """
    df = pd.read_csv(FILEPATH)
    if not any(df.channel_id == channel.id):
        df = pd.concat(
            [df, pd.DataFrame({"channel_id": [channel.id]})],
            ignore_index=True,
        )
        df.to_csv(FILEPATH, index=False)

def delete_subscribed_channel(channel):
    """
    Deletes the given channel from the repo.

    Args:
        channel: discord.py discord.abc.GuildChannel
    """
    df_subs = pd.read_csv(FILEPATH)
    df_subs = df_subs.drop(df_subs[df_subs['channel_id'] == channel.id].index)

    df_subs.to_csv(FILEPATH, index=False)