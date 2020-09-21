import yaml, sympy, googletrans
from discord.ext import commands

config = yaml.full_load(open("config.yml"))


class Util(commands.Cog, name=config["util"]["name"]):

    "Utilities that are not designed for fun."

    def __init__(self, bot):
        "Utilities that are not designed for fun."
        self.bot = bot

    @commands.command(
        name="calc",
        help=config["calc"]["help"],
        brief=config["calc"]["brief"],
        aliases=config["calc"]["aliases"],
        enabled=config["calc"]["enabled"],
        hidden=config["calc"]["hidden"],
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
        help=config["trans"]["help"],
        brief=config["trans"]["brief"],
        aliases=config["trans"]["aliases"],
        enabled=config["trans"]["enabled"],
        hidden=config["trans"]["hidden"],
    )
    async def trans(self, ctx, text: str, dest: str, src: str = "auto"):
        await ctx.send(
            "{} :abc:\n> {}".format(
                ctx.author.mention,
                googletrans.Translator().translate(text, dest, src).text,
            )
        )


def setup(bot):
    bot.add_cog(Util(bot))


def teardown(bot):
    bot.remove_cog(config["util"]["name"])
