"""Fun commands that are not games."""
import typing
import datetime
import googletrans
import google_trans_new
import operator
import random
import toml
import discord
from discord.ext import (
    commands,
)

config = toml.load("config.toml")
translator = google_trans_new.google_translator()


class Fun(
    commands.Cog,
    name=config["fun"]["name"],
    description=config["fun"]["description"],
):
    """Fun commands that are not games."""

    def __init__(
        self,
        bot: commands.AutoShardedBot,
    ):
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
        self, ctx: commands.Context, src: str, count: int, dest: str, *, text: str
    ):
        """Badly translate a word or sentence to another language."""
        if count > config["badgt"]["limit"]:
            await ctx.send(random.choice(config["badgt"]["warnings"]))
            return
        (prev, result,) = (
            src,
            text,
        )
        for lang in random.choices(
            googletrans.LANGUAGES,
            k=count,
        ):
            result = translator.translate(
                result,
                lang_tgt=lang,
                lang_src=prev,
            )
            prev = lang
        await ctx.send(
            translator.translate(
                result,
                lang_tgt=dest,
                lang_src=prev,
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
    async def slap(
        self,
        ctx: commands.Context,
        users: commands.Greedy[
            typing.Union[
                discord.Member,
                discord.User,
            ]
        ],
    ):
        """Slaps somebody."""
        await ctx.send(
            "You slapped {}.".format(
                ", ".join([str(_) for _ in users]),
            )
        )

    @commands.command(
        name="game",
        enabled=config["game"]["enabled"],
        hidden=config["game"]["hidden"],
        help=config["game"]["help"],
        brief=config["game"]["brief"],
        usage=config["game"]["usage"],
        aliases=config["game"]["aliases"],
    )
    async def game(
        self,
        ctx: commands.Context,
    ):
        """Plays the game."""
        if random.random() > config["game"]["win-chance"]:
            await ctx.send("I lost the game.")
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="xkcd: Anti-Mindvirus",
                    url="https://xkcd.com/391/",
                ).set_image(url="https://imgs.xkcd.com/comics/anti_mind_virus.png")
            )

    async def get_necro(
        self,
        nec: discord.TextChannel,
        posts: typing.Optional[int] = config["necro"]["posts"],
    ):
        (prev, score,) = (
            None,
            dict(),
        )
        if posts <= 0:
            hist = await nec.history(limit=None).flatten()
        else:
            hist = await nec.history(limit=posts).flatten()
        for post in hist:
            if post.author.bot and not config["necro"]["bot"]:
                continue
            if prev:
                if prev.author not in score:
                    score[prev.author] = datetime.timedelta()
                score[prev.author] += prev.created_at - post.created_at
            prev = post
        return score

    @commands.group(
        name="necro",
        enabled=config["necro"]["enabled"],
        hidden=config["necro"]["hidden"],
        help=config["necro"]["help"],
        brief=config["necro"]["brief"],
        usage=config["necro"]["usage"],
        aliases=config["necro"]["aliases"],
    )
    async def necro(
        self,
        ctx: commands.Context,
    ):
        pass

    @necro.command(name="rank")
    async def rank(
        self,
        ctx: commands.Context,
        nec: discord.TextChannel,
        posts: typing.Optional[int] = config["necro"]["posts"],
    ):
        score: dict = await self.get_necro(
            nec,
            posts,
        )
        if ctx.author in score:
            await ctx.send(
                "You necroposted for {}.".format(
                    str(score[ctx.author]),
                )
            )
        else:
            await ctx.send("You don't seem to have valid posts!")

    @necro.command(name="top")
    async def top(
        self,
        ctx: commands.Context,
        nec: discord.TextChannel,
        posts: typing.Optional[int] = config["necro"]["posts"],
    ):
        score: dict = await self.get_necro(
            nec,
            posts,
        )
        await ctx.send(
            "Here's the leaderboard you asked for:\n{}".format(
                "\n".join(
                    [
                        "{} - {}".format(
                            str(user),
                            str(time),
                        )
                        for (user, time,) in sorted(
                            score.items(),
                            key=operator.itemgetter(1),
                            reverse=True,
                        )
                    ]
                ),
            )
        )


def setup(
    bot: commands.AutoShardedBot,
):
    """Add the cog to the bot."""
    bot.add_cog(Fun(bot))


def teardown(
    bot: commands.AutoShardedBot,
):
    """Remove the cog from the bot."""
    bot.remove_cog(config["fun"]["name"])
