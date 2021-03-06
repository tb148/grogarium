"""Utilities that are not designed for fun."""
import googletrans
import google_trans_new
import sympy
import toml
from discord.ext import commands

config = toml.load("config.toml")
translator = google_trans_new.google_translator()


class Util(commands.Cog, name="Utilities"):
    """Utilities that are not designed for fun."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot

    @commands.command(
        name="calc",
        enabled=config["calc"]["enabled"],
        hidden=config["calc"]["hidden"],
        help=config["calc"]["help"],
        brief=config["calc"]["brief"],
        usage=config["calc"]["usage"],
        aliases=config["calc"]["aliases"],
    )
    async def calc(self, ctx, *, expression: str):
        """Calculate and/or simplify mathematical expressions. Certain symbols may be used."""
        expression = "".join(expression.strip("`").split("\\"))
        sympy.symbols("x y z t")
        sympy.symbols("k m n", integer=True)
        sympy.symbols("f g h", cls=sympy.Function)
        await ctx.send(
            "{} :1234:\n```{} = {}```".format(
                ctx.author.mention,
                expression,
                sympy.simplify(sympy.sympify(expression)),
            )
        )

    @commands.command(
        name="trans",
        enabled=config["trans"]["enabled"],
        hidden=config["trans"]["hidden"],
        help=config["trans"]["help"],
        brief=config["trans"]["brief"],
        usage=config["trans"]["usage"],
        aliases=config["trans"]["aliases"],
    )
    async def trans(self, ctx, src: str, dest: str, *, text: str):
        """Translate a word or sentence to another language."""
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                translator.translate(text, lang_tgt=dest, lang_src=src),
            )
        )

    @commands.command(
        name="langs",
        enabled=config["langs"]["enabled"],
        hidden=config["langs"]["hidden"],
        help=config["langs"]["help"],
        brief=config["langs"]["brief"],
        usage=config["langs"]["usage"],
        aliases=config["langs"]["aliases"],
    )
    async def langs(self, ctx):
        """Output a list that contains all the langcodes you can use."""
        await ctx.send(
            "{} :abc: Here's all the langcodes you can use:\n{}".format(
                ctx.author.mention,
                ", ".join(
                    [
                        "{} - {}".format(_, googletrans.LANGUAGES[_])
                        for _ in googletrans.LANGUAGES
                    ]
                ),
            )
        )


def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Util(bot))


def teardown(bot):
    """Remove the cog from the bot."""
    bot.remove_cog("Utilities")
