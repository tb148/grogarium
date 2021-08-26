"""Fun commands that are not games."""
import typing
import datetime
import googletrans
import operator
import random
import toml
import discord
from discord.ext import (
    commands,
)

config = toml.load("config.toml")
translator = googletrans.Translator()


class Fun(
    commands.Cog,
    name=config["fun"]["name"],
    description=config["fun"]["description"],
):
    """Fun commands that are not games."""

    def __init__(
        self,
        bot: commands.Bot,
    ):
        """Initialize the cog."""
        self.bot = bot

    @commands.command(
        name="badgt",
        enabled=config["badgt"]["enabled"],
        hidden=config["badgt"]["hidden"],
        help=config["badgt"]["help"],
        aliases=config["badgt"]["aliases"],
    )
    async def badgt(
        self,
        ctx: commands.Context,
        src: str,
        count: int,
        dest: str,
        *,
        text: str
    ):
        """Badly translate a word or sentence to another language."""
        if count > config["badgt"]["limit"]:
            await ctx.send(random.choice(config["badgt"]["warnings"]))
            return
        prev: str = src
        result: str = text
        async with ctx.typing():
            for lang in random.choices(
                list(googletrans.LANGUAGES.keys()),
                k=count,
            ):
                result = translator.translate(
                    result,
                    dest=lang,
                    src=prev,
                ).text
                prev = lang
            await ctx.send(
                translator.translate(
                    result,
                    dest=dest,
                    src=prev,
                ).text
            )

    @commands.command(
        name="slap",
        enabled=config["slap"]["enabled"],
        hidden=config["slap"]["hidden"],
        help=config["slap"]["help"],
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
                ).set_image(
                    url="https://imgs.xkcd.com/comics/anti_mind_virus.png"
                )
            )

    async def get_necro(
        self,
        ctx: commands.Context,
        nec: discord.TextChannel,
        posts: typing.Optional[int] = config["necro"]["posts"],
    ):
        async with ctx.typing():
            prev = None
            score = dict()
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
        case_insensitive=config["case-insensitive"],
        enabled=config["necro"]["enabled"],
        hidden=config["necro"]["hidden"],
        help=config["necro"]["help"],
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
        if posts > config["necro"]["limit"]:
            await ctx.send(random.choice(config["badgt"]["warnings"]))
            return
        score: dict = await self.get_necro(
            ctx,
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
        if posts > config["necro"]["limit"]:
            await ctx.send(random.choice(config["badgt"]["warnings"]))
            return
        score: dict = await self.get_necro(
            ctx,
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
    bot: commands.Bot,
):
    """Add the cog to the bot."""
    bot.add_cog(Fun(bot))


def teardown(
    bot: commands.Bot,
):
    """Remove the cog from the bot."""
    bot.remove_cog(config["fun"]["name"])
