"""Fun commands that are not games."""
import typing
import datetime
import googletrans
import google_trans_new
import operator
import random
import toml
import discord
from discord.ext import commands

config = toml.load("config.toml")
translator = google_trans_new.google_translator()


class Fun(commands.Cog, name="Fun"):
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
    async def badgt(self, ctx, src: str, count: int, dest: str, *, text: str):
        """Badly translate a word or sentence to another language."""
        if count > config["badgt"]["limit"]:
            await ctx.send(
                "{} :abc: {}\n".format(
                    ctx.author.mention, random.choice(config["badgt"]["warnings"])
                )
            )
            return
        prev, result = src, text
        for lang in random.choices([_ for _ in googletrans.LANGUAGES], k=count):
            result = translator.translate(result, lang_tgt=lang, lang_src=prev)
            prev = lang
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                translator.translate(result, lang_tgt=dest, lang_src=prev),
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
        self, ctx, users: commands.Greedy[typing.Union[discord.Member, discord.User]]
    ):
        """Slaps somebody."""
        await ctx.send(
            "{} :hand_splayed: You slapped {}.".format(
                ctx.author.mention,
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
    async def game(self, ctx):
        """Plays the game."""
        if random.random() > config["game"]["win-chance"]:
            await ctx.send(
                "{} :negative_squared_cross_mark: I lost the game. (https://en.wikipedia.org/wiki/The_Game_(mind_game))".format(
                    ctx.author.mention,
                ),
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="xkcd: Anti-Mindvirus",
                    description="I'm as surprised as you!  I didn't think it was possible.",
                    url="https://xkcd.com/391/",
                ).set_image(url="https://imgs.xkcd.com/comics/anti_mind_virus.png")
            )

    @commands.command(
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
        ctx,
        nec: discord.TextChannel,
        posts: typing.Optional[int] = config["necro"]["posts"],
        top: typing.Optional[bool] = config["necro"]["top"],
    ):
        prev, score, cnt = None, {}, 0
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
            if post.author == ctx.author:
                cnt += 1
            prev = post
        if top:
            await ctx.send(
                "{} :stadium: Here's the leaderboard you asked for:\n{}".format(
                    ctx.author.mention,
                    "\n".join(
                        [
                            "{} - {}".format(str(user), str(time))
                            for (user, time) in sorted(
                                score.items(), key=operator.itemgetter(1), reverse=True
                            )
                        ]
                    ),
                )
            )
        else:
            if ctx.author in score:
                await ctx.send(
                    "{} :stopwatch: You necroposted for {} using {} posts, which is {} per post.".format(
                        ctx.author.mention,
                        str(score[ctx.author]),
                        cnt,
                        str(score[ctx.author] / cnt),
                    )
                )
            else:
                await ctx.send(
                    "{} :negative_squared_cross_mark: You don't seem to have valid posts!".format(
                        ctx.author.mention
                    )
                )


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Fun(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog("Fun")
