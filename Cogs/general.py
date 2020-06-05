import json

import discord
from discord.ext import commands

class General(commands.Cog, name = "General"):
    def __init__(self, bot):
        self.bot = bot

        with open('./Data/bot.json', 'r+') as file:
            content = file.read()
            if len(content) == 0:
                self.bot.prefix = '!'
            else:
                data = json.loads(content)
                self.bot.prefix = data['prefix']

        print("Loaded General Cog")

    def cog_unload(self):
        print("Unloaded General Cog")

    @commands.command(name = "prefix", help = "Change the bot's prefix.", brief = "?")
    async def prefix(self, ctx, prefix: str):
        await ctx.trigger_typing()

        old_prefix = self.bot.prefix
        new_prefix = prefix
        self.bot.prefix = new_prefix

        with open('./Data/bot.json', 'w+') as file:
            file.write(json.dumps({"prefix": self.bot.prefix}, sort_keys = True, indent = 2))

        embed = discord.Embed(
            title = "Prefix Updated",
            color = self.bot.color
        )
        embed.add_field(
            name = "New Prefix",
            value = f"`{self.bot.prefix}`",
            inline = True
        )
        embed.add_field(
            name = "Example",
            value = f"`{self.bot.prefix}command`",
            inline = True
        )
        await ctx.send(embed = embed)

    @commands.command(name = "restart", help = "Restart the bot.", brief = "")
    async def restart(self, ctx):
        await ctx.message.add_reaction('✅')
        await self.bot.close()

def setup(bot):
    bot.add_cog(General(bot))
