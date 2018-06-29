#!/bin/env python3

import asyncio
import discord
import logging
import random
import re
import requests
from colorama import Fore, Style
from discord.ext.commands import Bot
from discord.ext import commands
from weather import Unit, Weather

enabled_exts = [
    "cogs.bee",
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
weather_ = Weather(unit=Unit.CELSIUS)

### COMMANDS ###

@bot.command()
async def weather(ctx, *location):
    raw_location = " ".join(location)
    response = weather_.lookup_by_location(raw_location)
    if response is None:
        await ctx.send(f"Unknown location '{raw_location}'")
        return

    condition = response.condition()

    await ctx.send("Weather for {}, {}: {}, {}°C, wind: {:.2f} km/h".format(
        response.location().city(), response.location().country(),
        condition.text(), condition.temp(), float(response.wind()["speed"])))

@bot.command()
async def insult(ctx, target : discord.Member):
    try:
        url = "https://evilinsult.com/generate_insult.php?lang=en"
        res = requests.get(url)
        insult = str(res.content, encoding="utf-8")
    except:
        logging.exception("Insult fetching failed")
        return

    await ctx.send(f"{target.mention}: {insult}")

@bot.command()
@commands.is_owner()
async def purge(ctx, number : int):
    await ctx.channel.purge(limit=number)

@bot.event
async def on_ready():
    print("Logged in ({}/{})".format(bot.user.name, bot.user.id))
    await bot.change_presence(game=discord.Game(name="with a bee"))

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    channel = message.channel

    if any(x == message.content for x in ['J', 'j']):
        await channel.send(message.content)

    m = re.search("store.steampowered.com/app/([0-9]+)", message.content)
    if m:
        await channel.send("steam://store/{}".format(m[1]))

@bot.listen()
async def on_message_delete(message):
    if message.author == bot.user:
        return

    await message.channel.send("{}: u little piece of shit >:("
            .format(message.author.mention))

for ext in enabled_exts:
    try:
        bot.load_extension(ext)
    except:
        logging.exception(f"Failed to load '{ext}'")


bot.run(token)
