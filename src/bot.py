import discord, toml, argparse, logging, random, aiohttp, time, typing
from discord.ext import commands, tasks

config = toml.load("config.toml")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--token",
    metavar="TOKEN",
    required=True,
    help="Your bot token. Keep this secret.",
)
parser.add_argument(
    "-p",
    "--prefix",
    metavar="PREFIX",
    default=config["prefix"],
    help="Bot prefix. Used to invoke the bot commands. Defaults to !$*",
)
parser.add_argument(
    "-v",
    "--verbose",
    metavar="VERBOSITY",
    default=1,
    help="Verbosity. -v for default logging, -vv for more logging, -vvv for debug logging.",
)
parser.add_argument(
    "-l",
    "--log",
    metavar="LOGFILE",
    default=config["logfile"],
    type=open,
    help="The path to store the logs.",
)
arg = parser.parse_args()
token, prefix, verbosity, logfile = arg.token, arg.prefix, arg.verbose, arg.log
logging.basicConfig(level=40 - 10 * verbosity, filename=logfile)
bot = commands.Bot(
    command_prefix=prefix,
    case_insensitive=config["case-insensitive"],
    description=config["description"],
    owner_ids=config["owners"],
)


@bot.command(
    name="roll",
    enabled=config["roll"]["enabled"],
    hidden=config["roll"]["hidden"],
    help=config["roll"]["help"],
    brief=config["roll"]["brief"],
    usage=config["roll"]["usage"],
    aliases=config["roll"]["aliases"],
)
async def roll(ctx, sizes: Greedy[int] = [6]):
    if len(sizes) == 2:
        if sizes[0] < 1 or sizes[1] > config["roll"]["limits"]["count"]:
            await ctx.send(
                "{} :game_die: {}".format(
                    random.choice(config["roll"]["warnings"]["limits"])
                )
            )
        sizes = [sizes[1] for _ in range(1, sizes[0])]
    if (
        len(sizes) == 0
        or len(sizes) > config["roll"]["limits"]["count"]
        or min(sizes) < 1
        or max(sizes) > config["roll"]["limits"]["size"]
    ):
        await ctx.send(
            "{} :game_die: {}".format(
                random.choice(config["roll"]["warnings"]["limits"])
            )
        )
    if (
        max(sizes) == 1
        and not config["roll"]["one-faced"]["max"]
        or min(sizes) == 1
        and not config["roll"]["one-faced"]["min"]
    ):
        await ctx.send(
            "{} :game_die: {}".format(
                random.choice(config["roll"]["warnings"]["one-faced"])
            )
        )
    dice = [random.randint(1, _) for _ in sizes]
    await ctx.send(
        "{} :game_die: You rolled a {}!\n```{}```".format(
            ctx.author.mention, sum(dice), ", ".join([str(_) for _ in dice])
        )
    )


@bot.command(
    name="8ball",
    enabled=config["8ball"]["enabled"],
    hidden=config["8ball"]["hidden"],
    help=config["8ball"]["help"],
    brief=config["8ball"]["brief"],
    usage=config["8ball"]["usage"],
    aliases=config["8ball"]["aliases"],
)
async def eight_ball(ctx, *, question: str):
    await ctx.send(
        "{} :8ball: {}\n> {}".format(
            ctx.author.mention, random.choice(config["8ball"]["answers"]), question
        )
    )


@bot.command(
    name="ping",
    enabled=config["ping"]["enabled"],
    hidden=config["ping"]["hidden"],
    help=config["ping"]["help"],
    brief=config["ping"]["brief"],
    usage=config["ping"]["usage"],
    aliases=config["ping"]["aliases"],
)
async def ping(ctx, *, url: typing.Optional[str] = config["ping"]["url"]):
    aio = aiohttp.ClientSession()
    pre = time.time()
    async with aio.get(url):
        res = time.time() - pre
    await ctx.channel.send(
        "{} :ping_pong: Pong!\nThe ping took {}ms.".format(
            ctx.author.mention, round(res * 1000)
        )
    )
    aio.close()


@tasks.loop(seconds=config["stat-freq"])
async def status():
    await bot.change_presence(activity=discord.Game(random.choice(config["status"])))


@bot.event
async def on_ready():
    print(random.choice(config["ready"]))
    status.start()


@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send(
        "{} {}\n```{}```".format(
            ctx.author.mention, random.choice(config["error"]), error
        )
    )


bot.load_extension("util")
bot.run(token)
