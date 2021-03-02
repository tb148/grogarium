"""Use this bot as an user."""
import toml
import typing
import discord
from discord.ext import commands

config = toml.load("config.toml")


class Usr(
    commands.Cog,
    name=config["usr"]["name"],
    description=config["usr"]["description"],
    command_attrs={hidden: True},
):
    """Use this bot as an user."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot

    @commands.command(name="send")
    @commands.is_owner()
    async def send(self, ctx, tchannel: discord.TextChannel, *, msg: str):
        """Send something."""
        await tchannel.send(msg)
        await ctx.send("Sent {} to {}.".format(msg, tchannel.name))

    @commands.command(name="erase")
    @commands.is_owner()
    async def erase(self, ctx, msg: discord.Message, time: typing.Optional[float]):
        """Delete a message."""
        await msg.delete(delay=time)
        await ctx.send("Deleted the message.")

    @commands.command(name="edit")
    @commands.is_owner()
    async def edit(self, ctx, msg: discord.Message, *, text: str):
        """Delete a message."""
        await msg.edit(text)
        await ctx.send("Edit the message to {}.".format(text))


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Usr(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog("User")
