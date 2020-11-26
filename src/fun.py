"""Fun commands that are not games."""
import typing

import googletrans
import random
import toml
from discord.ext import commands

config = toml.load("config.toml")


class Fun(commands.Cog, name=config["fun"]["name"]):
    """Fun commands that are not games."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot

    @commands.command(
        name="badgt",
        enabled=config["badgt"]["enabled"],
        hidden=config["badgt"]["hidden"],
        help=config["badgt"]["help"],
        brief=config["badgt"]["brief"],
        usage=config["badgt"]["usage"],
        aliases=config["badgt"]["aliases"],
    )
    async def badgt(
        self, ctx, count: int, dest: str,* , text
    ):
        """Badly translate a word or sentence to another language."""
        for _ in range(count):
          text=googletrans.Translator().translate(text, random.choice([_ for _ in googletrans.LANGUAGES]), "auto").text
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                googletrans.Translator().translate(text, dest, "auto").text
            )
        )



def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Fun(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog(config["fun"]["name"])
