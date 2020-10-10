"Utilities that are not designed for fun."
import typing
import googletrans
import sympy
import toml
from discord.ext import commands

config = toml.load("config.toml")


class Util(commands.Cog, name=config["util"]["name"]):
    "Utilities that are not designed for fun."

    def __init__(self, bot):
        "Initialize the cog."
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
        "Calculate and/or simplify mathematical expressions. Certain symbols may be used."
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
    async def trans(
        self, ctx, text: str, dest: str, src: typing.Optional[str] = "auto"
    ):
        "Translate a word or sentence to another language."
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                googletrans.Translator().translate(text, dest, src).text,
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
        "Output a list that contains all the langcodes you can use."
        await ctx.send(
            "{} :abc: {}\n{}".format(
                ctx.author.mention,
                config["langs"]["message"],
                "\n".join(
                    [
                        "{} - {}".format(_, googletrans.LANGUAGES[_])
                        for _ in googletrans.LANGUAGES
                    ]
                ),
            )
        )


def setup(bot):
    "Add the cog to the bot."
    bot.add_cog(Util(bot))


def teardown(bot):
    "Remove the cog from the bot."
    bot.remove_cog(config["util"]["name"])
