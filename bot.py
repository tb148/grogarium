"""The main file for the bot."""
import argparse
import logging
import os
import random

import discord
import toml
from discord.ext import (
    commands,
    tasks,
)

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
    "-v",
    "--verbose",
    default=1,
    action="count",
    help="Verbosity. More v means more verbose logging.",
)
parser.add_argument(
    "-l",
    "--logfile",
    default="grogar.log",
    help="The file to write logs to.",
)
arg = parser.parse_args()
(token, verbosity, logfile,) = (
    arg.token,
    arg.verbose,
    arg.logfile,
)
logging.basicConfig(
    level=40 - 10 * verbosity,
    filename=logfile,
)
bot = commands.AutoShardedBot(
    command_prefix=commands.when_mentioned_or("Gr!"),
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
async def roll(
    ctx,
    sizes: commands.Greedy[int],
):
    """Roll some dice."""
    if len(sizes) == 0:
        sizes = [6]
    if len(sizes) == 2:
        if sizes[0] < 1 or sizes[1] > config["roll"]["limits"]["count"]:
            await ctx.reply(
                content="{} :game_die: {}".format(
                    ctx.author.mention,
                    random.choice(config["roll"]["warnings"]["limits"]),
                )
            )
            return
        sizes = [sizes[1] for _ in range(sizes[0])]
    if (
        len(sizes) > config["roll"]["limits"]["count"]
        or min(sizes) < 1
        or max(sizes) > config["roll"]["limits"]["size"]
    ):
        await ctx.reply(
            content="{} :game_die: {}".format(
                ctx.author.mention,
                random.choice(config["roll"]["warnings"]["limits"]),
            )
        )
        return
    if (
        max(sizes) == 1
        and not config["roll"]["one-faced"]["every"]
        or min(sizes) == 1
        and not config["roll"]["one-faced"]["any"]
    ):
        await ctx.reply(
            content="{} :game_die: {}".format(
                ctx.author.mention,
                random.choice(config["roll"]["warnings"]["one-faced"]),
            )
        )
        return
    dice = [
        random.randint(
            1,
            _,
        )
        for _ in sizes
    ]
    await ctx.reply(
        content="{} :game_die: You rolled a {}!\n```{}```".format(
            ctx.author.mention,
            sum(dice),
            ", ".join([str(_) for _ in dice]),
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
    """Ask a question, get an answer."""
    await ctx.reply(
        content="{} :8ball: {}\n> {}".format(
            ctx.author.mention,
            random.choice(config["8ball"]["answers"]),
            question,
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
async def ping(
    ctx,
):
    """Test the internet connection of the bot."""
    await ctx.reply(
        content="{} :ping_pong: Pong!\n{}".format(
            ctx.author.mention,
            " ".join(
                [
                    "Pinging shard {} took {}ms.".format(
                        shard_id,
                        round(latency * 1000),
                    )
                    for (
                        shard_id,
                        latency,
                    ) in bot.latencies
                ]
            ),
        )
    )


@tasks.loop(seconds=config["stat-freq"])
async def status():
    """Change the status of the bot."""
    await bot.change_presence(
        activity=discord.Game(random.choice(config["status"]))
    )


@bot.event
async def on_ready():
    """Tell the owner that the bot is ready."""
    for filename in os.listdir("./src"):
        if filename.endswith(".py"):
            bot.load_extension("src.{}".format(filename[:-3]))
    print(random.choice(config["ready"]))
    status.start()


@bot.event
async def on_command_error(
    ctx,
    error,
):
    """Tell the user that an error occured."""
    await ctx.channel.send(
        "{} {}\n```{}```".format(
            ctx.author.mention,
            random.choice(config["error"]),
            error,
        )
    )


bot.run(token)
