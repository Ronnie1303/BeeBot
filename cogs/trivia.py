import asyncio
import discord
import random
from datetime import datetime
from discord.ext import commands


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.triviaDictFile = "trivia.txt"

    @commands.command()
    async def trivia(self, ctx):
        trivia = open(self.triviaDictFile, "r").read().splitlines()
        random.seed(hash(datetime.now()))
        response = random.choice(trivia)

        await ctx.send(response)


def setup(bot):
    bot.add_cog(Trivia(bot))
