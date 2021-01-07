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
        async with aiohttp.ClientSession() as session:
            async with session.get("https://thispersondoesnotexist.com/image") as resp:
                if resp.status != 200:
                    return await ctx.send("Could not download file...")
                await ctx.send(
                    file=discord.File(io.BytesIO(await resp.read()), "cool_image.jpeg")
                )


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Imag(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog("This Object Does Not Exist")
