import discord, yaml, sys, getopt, logging, random, aiohttp, time
from discord.ext import commands, tasks

config = yaml.full_load(open("config.yml"))
opts, args = getopt.getopt(sys.argv[1:], "t:p:c", ["token=", "prefix=", "case"])
for opt, arg in opts:
    if opt in ("-t", "--token"):
        token = arg
    elif opt in ("-p", "--prefix"):
        config["prefix"] = arg
    elif opt in ("-c", "--case"):
        config["case-insensitive"] = True
bot = commands.Bot(
    command_prefix=config["prefix"],
    case_insensitive=config["case-insensitive"],
    description=config["description"],
    owner_ids=config["owners"],
)


@bot.command(
    name="roll",
    help=config["roll"]["help"],
    brief=config["roll"]["brief"],
    aliases=config["roll"]["aliases"],
    enabled=config["roll"]["enabled"],
    hidden=config["roll"]["hidden"],
)
async def roll(
    ctx,
    count: int = config["roll"]["default"]["count"],
    size: int = config["roll"]["default"]["size"],
):
    if (
        count > config["roll"]["limits"]["count"]
        or size > config["roll"]["limits"]["size"]
        or count < 1
        or size < 1
    ):
        await ctx.send(
            "{} :game_die: {}".format(
                ctx.author.mention, random.choice(config["roll"]["warnings"]["limits"])
            )
        )
        return
    if size == 1 and not config["roll"]["one-faced"]:
        await ctx.send(
            "{} :game_die: {}".format(
                ctx.author.mention,
                random.choice(config["roll"]["warnings"]["one-faced"]),
            )
        )
        return
    dice = list()
    tot = 0
    for i in range(count):
        res = random.randint(1, size)
        tot += res
        dice.append(str(res))
    await ctx.send(
        "{} :game_die: You rolled a {}!\n```{}```".format(
            ctx.author.mention, tot, ", ".join(dice)
        )
    )


@bot.command(
    name="8ball",
    help=config["8ball"]["help"],
    brief=config["8ball"]["brief"],
    aliases=config["8ball"]["aliases"],
    enabled=config["8ball"]["enabled"],
    hidden=config["8ball"]["hidden"],
)
async def eight_ball(ctx, *, question: str):
    await ctx.send(
        "{} :8ball: {}\n> {}".format(
            ctx.author.mention, random.choice(config["8ball"]["answers"]), question
        )
    )


@bot.command(
    name="ping",
    help=config["ping"]["help"],
    brief=config["ping"]["brief"],
    aliases=config["ping"]["aliases"],
    enabled=config["ping"]["enabled"],
    hidden=config["ping"]["hidden"],
)
async def ping(ctx, *, url: str = config["ping"]["url"]):
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
            ctx.author.mention, random.choice(config["error"]), type(error)
        )
    )


bot.load_extension("util")
bot.run(token)
