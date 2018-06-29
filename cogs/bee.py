import asyncio
import discord
import random

bee_emoji = "🐝"
quotes = {
    "Ray Bradbury" : "Bees do have a smell, you know, and if they don’t they should, for their feet are dusted with spices from a million flowers.",
    "Muriel Barbery" : "We think we can make honey without sharing in the fate of bees, but we are in truth nothing but poor bees, destined to accomplish our task and then die.",
    "William Longgood" : "The bee is domesticated but not tamed.",
    "Marcus Aurelius" : "That which is not good for the bee-hive cannot be good for the bees.",
    "William Blake" : "The busy bee has no time for sorrow.",
    "Brother Adam" : "Listen to the bees and let them guide you.",
    "St John Chrysostom" : "The bee is more honoured than other animals,not because she labors,but because she labours for others.",
    "Congolese" : "When the bee comes to your house, let her have beer; you may want to visit the bee’s house some day.",
    "Eddie Izzard" : "I'm covered in bees!",
    "Ralph Waldo Emerson" : "God will not have his work made manifest by cowards.",
    "Miloš Zeman" : "Kunda sem, kunda tam...",
}

class Bee:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        channel = message.channel

        if "bee" in message.content.lower():
            await message.add_reaction(bee_emoji)

        if message.content.lower() == "bee":
            author, quote = random.choice(list(quotes.items()))
            await channel.send("*\"{}\"* - {}".format(quote, author))


def setup(bot):
    bot.add_cog(Bee(bot))
