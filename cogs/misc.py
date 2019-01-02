import asyncio
import discord
from discord.ext import commands

letters_emoji = ["🇩", "🇪", "🇸", "🇵", "🇦", "🇨", "🇮", "🇹", "🇴"]

class Misc:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "bee play despacito" in message.content.lower() or "bee, play despacito" in message.content.lower():
            channel = message.channel
            for letter in letters_emoji:
                await message.add_reaction(letter)
            await channel.send("https://www.youtube.com/watch?v=kJQP7kiw5Fk")


def setup(bot):
    bot.add_cog(Misc(bot))
