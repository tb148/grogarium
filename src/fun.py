"""Fun commands that are not games."""
import typing

import googletrans
import random
import toml
import discord
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
    async def badgt(self, ctx, count: int, dest: str, *, text: str):
        """Badly translate a word or sentence to another language."""
        result = text
        for lang in random.choices([_ for _ in googletrans.LANGUAGES], k=count):
            result = googletrans.Translator().translate(result, lang, "auto").text
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                googletrans.Translator().translate(result, dest, "auto").text,
            )
        )
    
    @commands.command(
        name="slap",
        enabled=config["slap"]["enabled"],
        hidden=config["slap"]["hidden"],
        help=config["slap"]["help"],
        brief=config["slap"]["brief"],
        usage=config["slap"]["usage"],
        aliases=config["slap"]["aliases"],
    )
    async def slap(self, ctx, users: commands.Greedy[typing.Union[discord.Member,discord.User]]):
        """Slaps somebody."""
        await ctx.send(
            "{} :hand_splayed: You slapped {}.".format(
                ctx.author.mention,
                ", ".join(users)
            )
        )
        
    



def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Fun(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog(config["fun"]["name"])
