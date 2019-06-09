#!/bin/env python3

import asyncio
import discord
import logging
from discord.ext import commands
from discord.ext.commands import Bot
from colorama import Fore, Style

enabled_exts = [
    "cogs.bee",
    "cogs.other",
    "cogs.steam",
    "cogs.trivia",
    "cogs.weather",
    "cogs.misc",
]

# Setup logging
logging_colors = {
    logging.DEBUG    : Fore.BLUE,
    logging.INFO     : Fore.GREEN,
    logging.WARNING  : Fore.YELLOW,
    logging.ERROR    : Fore.RED,
    logging.CRITICAL : Fore.MAGENTA
}
logging.basicConfig(level=logging.INFO,
        format="%(asctime)-15s [%(module)s/%(funcName)s] %(levelname)s: %(message)s")
for level, color in logging_colors.items():
    logging.addLevelName(level, "{}{}{}".format(color, logging.getLevelName(level),
            Style.RESET_ALL))

with open(".discord_token") as fp:
    token = fp.readline().strip()

bot = Bot(description="BeeBot", command_prefix="?")

@bot.event
async def on_command_error(ctx, exception):
    suppressed_exceptions = (
        commands.CommandNotFound,
        commands.errors.CommandInvokeError
    )
    selfdestruct_exceptions = (
        commands.CommandOnCooldown
    )
    selfdestruct = None

    logging.error("({}) {}".format(type(exception), exception))

    err = discord.Embed(title="Error", colour=0xdd5f53)

    # Silently ignore some exceptions
    if isinstance(exception, suppressed_exceptions):
        return

    # Delete selected error messages after x seconds along with CD'ed command
    if isinstance(exception, selfdestruct_exceptions):
        await ctx.message.delete()
        selfdestruct = 5

    # Replace the generic CheckFailure message with something more useful
    if isinstance(exception, commands.CheckFailure):
        err.description = "Insufficient permissions"
    else:
        err.description = str(exception)

    await ctx.send(embed=err, delete_after=selfdestruct)

@bot.event
async def on_ready():
    invite = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot" \
                .format(bot.user.id)
    gamename = "{}help".format(bot.command_prefix)
    logging.info("Invite link: {}".format(invite))
    logging.info("Logged in ({}/{})".format(bot.user.name, bot.user.id))
    await bot.change_presence(activity=discord.Game(name="with a bee"))
    servers = [s.name for s in bot.guilds]
    logging.info("Servers: {}".format(", ".join(servers)))

# Load cogs
for ext in enabled_exts:
    try:
        bot.load_extension(ext)
    except:
        logging.exception(f"Failed to load '{ext}'")


bot.run(token)
