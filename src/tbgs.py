"""Sync messages with TBGForums."""
import os
import requests
import toml
import discord
from discord.ext import commands, tasks

config = toml.load("config.toml")


class Tbgs(
    commands.Cog,
    name=config["tbgs"]["name"],
    description=config["tbgs"]["description"],
):
    """Sync messages with TBGForums."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot
        self.msg = ""
        self.url = "https://tbgforums.com/forums/"
        self.tbgs = requests.Session()
        form = {"form_sent": "1"}
        form["req_username"] = os.getenv("TBGS_USERNAME")
        form["req_password"] = os.getenv("TBGS_PASSWORD")
        form["login"] = "Login"
        self.tbgs.post(self.url + "login.php?action=in", data=form)
        self.autosync.start()

    def cog_unload(self):
        self.autosync.cancel()

    @commands.command(
        name="sync",
        enabled=config["sync"]["enabled"],
        hidden=config["sync"]["hidden"],
        help=config["sync"]["help"],
        brief=config["sync"]["brief"],
        usage=config["sync"]["usage"],
        aliases=config["sync"]["aliases"],
    )
    async def sync(self, ctx, msg: discord.Message):
        """Sync messages with TBGForums."""
        self.msg += "[quote={}]{}[/quote]".format(str(msg.author), msg.content)
        await ctx.send("Message {} added to queue.".format(msg.id))

    @tasks.loop(seconds=config["sync"]["sync-freq"])
    async def autosync(self):
        """Sync messages with TBGForums."""
        if self.msg == "":
            return
        form = {"form_sent": "1"}
        form["req_message"] = self.msg
        self.tbgs.post(
            self.url + "post.php?tid=" + os.getenv("TBGS_TOPICTID"), data=form
        )
        self.msg = ""


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Tbgs(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog(config["tbgs"]["name"])
