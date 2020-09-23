import yaml, sympy, googletrans, typing
from discord.ext import commands

config = yaml.full_load(open("config.yml"))


class Util(commands.Cog, name=config["util"]["name"]):

    "Utilities that are not designed for fun."

    def __init__(self, bot):
        "Utilities that are not designed for fun."
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
        sympy.symbols("x y z")
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
        await ctx.send(
            "{} :abc: {}\n{}".format(
                ctx.author.mention,
                "\n".join(
                    [
                        "{} - {}".format(_, googletrans.LANGUAGES[_])
                        for _ in googletrans.LANGUAGES
                    ]
                ),
            )
        )


def setup(bot):
    bot.add_cog(Util(bot))


def teardown(bot):
    bot.remove_cog(config["util"]["name"])
