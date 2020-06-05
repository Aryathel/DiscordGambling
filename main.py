import datetime
import os
import random

import discord
from discord.ext import commands

def get_prefix(bot, message):
    return bot.prefix

bot = commands.Bot(command_prefix=get_prefix, description = "Hero's Gambling.", ignore_case = True)

bot.TOKEN = os.getenv('Placeholder')
bot.log_channel_id = 601811847590576152
# Random embed color each time the bot is run
# bot.color = discord.Color.from_rgb(random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
bot.color = discord.Color.from_rgb(123, 240, 234)

extensions = [
    'Cogs.general',
    'Cogs.gambling'
]

for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    game = discord.Game(name = f"Serving {len(bot.guilds)} | {bot.prefix}help")
    await bot.change_presence(activity = game)

    bot.log_channel = bot.get_channel(bot.log_channel_id)

    embed = discord.Embed(
        title = f"{bot.user.name} Online!",
        timestamp = datetime.datetime.now(datetime.timezone.utc),
        color = bot.color
    )
    await bot.log_channel.send(embed = embed)

    print(f"Connected to Discord with user {bot.user}! (ID: {bot.user.id})")

bot.run(bot.TOKEN, reconnect = True, bot = True)
