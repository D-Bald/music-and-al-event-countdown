import pandas as pd
from disnake.abc import GuildChannel
from config import SUBSCRIPTIONS_FILEPATH

class Subscriptions():
    @staticmethod
    def all() -> list[int]:
        """
        Reads channel ids to be scheduled and returns them as list.

        Returns:
            List of ids of subscribed channels
        """
        df_subs = pd.read_csv(SUBSCRIPTIONS_FILEPATH)
        subs_list = df_subs["channel_id"].values.tolist()
        return subs_list

    @staticmethod
    def save(channel: GuildChannel):
        """
        Saves the given channel to be scheduled again on start-up.

        Args:
            guild_channel: disnake.abc.GuildChannel
        """
        df = pd.read_csv(SUBSCRIPTIONS_FILEPATH)
        if not any(df.channel_id == channel.id):
            df = pd.concat(
                [df, pd.DataFrame({"channel_id": [channel.id]})],
                ignore_index=True,
            )
            df.to_csv(SUBSCRIPTIONS_FILEPATH, index=False)

    @staticmethod
    def delete(channel: GuildChannel):
        """
        Deletes the given channel from the repo.

        Args:
            channel: disnake.abc.GuildChannel
        """
        df_subs = pd.read_csv(SUBSCRIPTIONS_FILEPATH)
        df_subs = df_subs.drop(df_subs[df_subs['channel_id'] == channel.id].index)

        df_subs.to_csv(SUBSCRIPTIONS_FILEPATH, index=False)
