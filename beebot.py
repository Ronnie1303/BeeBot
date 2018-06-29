#!/bin/env python3

import asyncio
import discord
import logging
import re
import requests
from colorama import Fore, Style
from discord.ext.commands import Bot
from discord.ext import commands

enabled_exts = [
    "cogs.bee",
    "cogs.other",
    "cogs.weather",
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

### COMMANDS ###

@bot.event
async def on_ready():
    invite = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot" \
                .format(bot.user.id)
    gamename = "{}help".format(bot.command_prefix)
    logging.info("Invite link: {}".format(invite))
    logging.info("Logged in ({}/{})".format(bot.user.name, bot.user.id))
    await bot.change_presence(game=discord.Game(name="with a bee"))
    servers = [s.name for s in bot.guilds]
    logging.info("Servers: {}".format(", ".join(servers)))

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    channel = message.channel

    m = re.search("store.steampowered.com/app/([0-9]+)", message.content)
    if m:
        await channel.send("steam://store/{}".format(m[1]))

for ext in enabled_exts:
    try:
        bot.load_extension(ext)
    except:
        logging.exception(f"Failed to load '{ext}'")


bot.run(token)
