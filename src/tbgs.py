"""Sync messages with TBGForums."""
import os
import requests
import toml
import discord
from discord.ext import (
    commands,
    tasks,
)

config = toml.load("config.toml")


class Tbgs(
    commands.Cog,
    name=config["tbgs"]["name"],
    description=config["tbgs"]["description"],
):
    """Sync messages with TBGForums."""

    def __init__(
        self,
        bot: commands.AutoShardedBot,
    ):
        """Initialize the cog."""
        self.bot: commands.AutoShardedBot = bot
        self.msg: str = ""
        self.url: str = "https://tbgforums.com/forums/"
        self.autosync.start()

    def cog_unload(
        self,
    ):
        self.autosync.cancel()

    def convert(
        self,
        src: str,
    ):
        res = ""
        pre = 0
        for c in src:
            if 0xE000 <= ord(c) < 0xF900 or ord(c) >= 0x10000:
                (hi, lo,) = divmod(
                    ord(c),
                    0x1000,
                )
                if hi != pre:
                    res += chr(hi + 0xF000)
                    pre = hi
                res += chr(lo + 0xE000)
            else:
                res += c
        return res

    @commands.command(
        name="sync",
        enabled=config["sync"]["enabled"],
        hidden=config["sync"]["hidden"],
        help=config["sync"]["help"],
        brief=config["sync"]["brief"],
        usage=config["sync"]["usage"],
        aliases=config["sync"]["aliases"],
    )
    async def sync(
        self,
        ctx: commands.Context,
        msg: discord.Message,
    ):
        """Sync messages with TBGForums."""
        if msg.content == "":
            await ctx.send("You can't sync files or embeds!")
            return
        if "[" in msg.content or "]" in msg.content:
            await ctx.send("You can't sync BBCode!")
            return
        self.msg += "[quote={}]{}[/quote]".format(
            str(msg.author),
            self.convert(msg.content),
        )
        await ctx.send(
            "Message {} added to queue.".format(
                msg.id,
            )
        )

    @tasks.loop(seconds=config["sync"]["sync-freq"])
    async def autosync(
        self,
    ):
        """Sync messages with TBGForums."""
        if self.msg != "":
            with requests.Session() as tbgs:
                form: dict = {"form_sent": "1"}
                form["req_username"] = os.getenv("TBGS_USERNAME")
                form["req_password"] = os.getenv("TBGS_PASSWORD")
                form["login"] = "Login"
                tbgs.post(
                    self.url + "login.php?action=in",
                    data=form,
                )
                form: dict = {"form_sent": "1"}
                form["req_message"] = self.msg
                tbgs.post(
                    self.url + "post.php?tid=" + os.getenv("TBGS_TOPICTID"),
                    data=form,
                )
                self.msg = ""


def setup(
    bot: commands.AutoShardedBot,
):
    """Add the cog to the bot."""
    bot.add_cog(Tbgs(bot))


def teardown(
    bot: commands.AutoShardedBot,
):
    """Remove the cog from the bot."""
    bot.remove_cog(config["tbgs"]["name"])
