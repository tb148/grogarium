"""Imaginary images generated by StyleGANs."""
import aiohttp
import io
import toml
import discord
from discord.ext import commands

config = toml.load("config.toml")


class Imag(commands.Cog, name="This Object Does Not Exist"):
    """Imaginary images generated by StyleGANs."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot

    async def get_imag(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return discord.File(io.BytesIO(await resp.read()), "cool_image.jpeg")

    @commands.command(
        name="human",
        enabled=config["human"]["enabled"],
        hidden=config["human"]["hidden"],
        help=config["human"]["help"],
        brief=config["human"]["brief"],
        usage=config["human"]["usage"],
        aliases=config["human"]["aliases"],
    )
    async def human(self, ctx):
        """This Person Does Not Exist."""
        await ctx.send(file=self.get_imag("https://thispersondoesnotexist.com/image"))

    @commands.command(
        name="arts",
        enabled=config["arts"]["enabled"],
        hidden=config["arts"]["hidden"],
        help=config["arts"]["help"],
        brief=config["arts"]["brief"],
        usage=config["arts"]["usage"],
        aliases=config["arts"]["aliases"],
    )
    async def arts(self, ctx):
        """This Artwork Does Not Exist."""
        await ctx.send(file=self.get_imag("https://thisartworkdoesnotexist.com"))

    @commands.command(
        name="cats",
        enabled=config["cats"]["enabled"],
        hidden=config["cats"]["hidden"],
        help=config["cats"]["help"],
        brief=config["cats"]["brief"],
        usage=config["cats"]["usage"],
        aliases=config["cats"]["aliases"],
    )
    async def cats(self, ctx):
        """This Cat Does Not Exist."""
        await ctx.send(file=self.get_imag("https://thiscatdoesnotexist.com"))

    @commands.command(
        name="horse",
        enabled=config["horse"]["enabled"],
        hidden=config["horse"]["hidden"],
        help=config["horse"]["help"],
        brief=config["horse"]["brief"],
        usage=config["horse"]["usage"],
        aliases=config["horse"]["aliases"],
    )
    async def horse(self, ctx):
        """This Horse Does Not Exist."""
        await ctx.send(file=self.get_imag("https://thishorsedoesnotexist.com"))


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Imag(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog("This Object Does Not Exist")
