import asyncio
import discord
import re
from discord.ext import commands

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        channel = message.channel

        m = re.search("store.steampowered.com/app/([0-9]+)", message.content)
        if m:
            await channel.send("steam://store/{}".format(m[1]))


def setup(bot):
    bot.add_cog(Steam(bot))
