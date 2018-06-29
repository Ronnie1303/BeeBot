import asyncio
import discord
from discord.ext import commands

class Other:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx, number : int):
        await ctx.channel.purge(limit=number)

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        channel = message.channel

        if any(x == message.content for x in ['J', 'j']):
            await channel.send(message.content)

    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        await message.channel.send("{}: u little piece of shit >:("
                .format(message.author.mention))


def setup(bot):
    bot.add_cog(Other(bot))
