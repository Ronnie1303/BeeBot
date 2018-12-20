import asyncio
import discord
from discord.ext import commands
from weather import Unit, Weather as LibWeather


class Weather:
    def __init__(self, bot):
        self.bot = bot
        self._weather = LibWeather(unit=Unit.CELSIUS)

    @commands.command()
    async def weather(self, ctx, *, location):
        response = self._weather.lookup_by_location(location)
        if response is None:
            await ctx.send(f"Unknown location '{raw_location}'")
            return

        condition = response.condition()

        await ctx.send("Weather for {}, {}: {}, {}°C, wind: {:.2f} km/h".format(
            response.location().city(), response.location().country(),
            condition.text(), condition.temp(), float(response.wind()["speed"])))


def setup(bot):
    bot.add_cog(Weather(bot))
