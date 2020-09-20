import discord, yaml, sympy
from discord.ext import commands

config = yaml.full_load(open("config.yml"))


class Util(commands.Cog, name=config["util"]["name"]):
    def __init__(self, bot):
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
            "{} :1234:\n{} = {}".format(
                ctx.author.mention,
                expression,
                sympy.simplify(sympy.sympify(expression)),
            )
        )


def setup(bot):
    bot.add_cog(Util(bot))


def teardown(bot):
    bot.remove_cog(config["util"]["name"])
