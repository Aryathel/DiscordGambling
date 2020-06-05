import datetime
import json
import random

import discord
from discord.ext import commands

class Gambling(commands.Cog, name = "Gambling"):
    def __init__(self, bot):
        self.bot = bot

        self.cooldown_in_hours = 2

        with open('./Data/gambling.json', 'r+') as file:
            content = file.read()
            if len(content) == 0:
                self.bot.gambling_data = {}
            else:
                self.bot.gambling_data = json.loads(content)

        print("Loaded Gambling Cog")

    def cog_unload(self):
        print("Unloaded Gambling Cog")

    @commands.command(name = 'beg', aliases = ['work'], help = "Earn a random amount of coins in the range 1-100 once every two hours.")
    async def beg(self, ctx):
        await ctx.trigger_typing()
        if str(ctx.author.id) in self.bot.gambling_data.keys():
            user_tokens = self.bot.gambling_data[str(ctx.author.id)]['tokens']
            cooldown = self.bot.gambling_data[str(ctx.author.id)]['cooldown']
        else:
            user_tokens = 0
            cooldown = None

        if cooldown:
            last_use = datetime.datetime.fromtimestamp(cooldown)
        else:
            last_use = None

        if last_use == None or datetime.datetime.now() > (last_use + datetime.timedelta(hours = self.cooldown_in_hours)):
            # User cooldown is over.
            num_tokens = random.randint(1, 100)
            user_tokens += num_tokens

            self.bot.gambling_data[str(ctx.author.id)] = {
                "tokens": user_tokens,
                "cooldown": datetime.datetime.now().timestamp()
            }

            with open('./Data/gambling.json', 'w+') as file:
                file.write(json.dumps(self.bot.gambling_data, sort_keys = True, indent = 2))

            embed = discord.Embed(
                title = f"{num_tokens} Coins Earned",
                color = self.bot.color
            )
            embed.add_field(
                name = 'Total Coins',
                value = user_tokens
            )
            await ctx.send(embed = embed)
        else:
            # User cooldown is still active.
            time_left = (last_use + datetime.timedelta(hours = self.cooldown_in_hours)).timestamp() - datetime.datetime.now().timestamp()
            time_left = round(time_left / 60)
            embed = discord.Embed(
                title = "Cooldown Active",
                description = f"You cannot use that command for another {time_left} minutes.",
                color = self.bot.color,
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.send(embed = embed)

    @commands.command(name = "coins", aliases = ['tokens', 't', 'c'], help = "View coins for yourself or another user.")
    async def tokens(self, ctx, *, member: discord.Member = None):
        await ctx.trigger_typing()

        if member == None:
            member = ctx.author

        if str(member.id) in self.bot.gambling_data.keys():
            # If a user has tokens
            embed = discord.Embed(
                title = f"{member.name}'s Coins",
                description = self.bot.gambling_data[str(member.id)]['tokens'],
                color = self.bot.color
            )
            await ctx.send(embed = embed)
        else:
            # If the user does not have tokens.
            embed = discord.Embed(
                title = f"{member.name} has no Coins",
                description = f"To get started earning coins, use `{self.bot.prefix}beg`.",
                color = self.bot.color
            )
            await ctx.send(embed = embed)

    @commands.command(name = "leaders", aliases = ['leaderboard', 'ldb'], help = "View the token leaderboard.")
    async def leaderboard(self, ctx):
        await ctx.trigger_typing()
        leaders = []
        i = 0
        user_pos = "You Have No Tokens"
        for id in reversed(sorted(self.bot.gambling_data.items(), key = lambda entry: entry[1]['tokens'])):
            user = self.bot.get_user(int(id[0]))
            if user:
                i += 1
                if int(id[0]) == ctx.author.id:
                    user_pos = f"**#{i}**"
                if len(leaders) < 10:
                    leaders.append(f"**#{i}:** {user.mention} `{self.bot.gambling_data[id[0]]['tokens']}`")

        embed = discord.Embed(
            title = "Coin Leaderboard",
            description = "\n".join(leaders),
            color = self.bot.color
        )
        embed.add_field(
            name = "Your Position",
            value = user_pos
        )
        await ctx.send(embed = embed)

    @commands.command(name = "gamble", aliases = ['bet'], help = "Gamble a certain amount of coins, double or nothing.", brief = "123")
    async def gamble(self, ctx, amount: int):
        await ctx.trigger_typing()
        amount = abs(amount)
        if str(ctx.author.id) in self.bot.gambling_data.keys():
            # User is in the data system
            if self.bot.gambling_data[str(ctx.author.id)]['tokens'] >= amount:
                user_tokens = self.bot.gambling_data[str(ctx.author.id)]['tokens']
                # User bet is allowed
                success = random.randint(1, 100)
                if success >= 1 and success < 49:
                    # Failed
                    user_tokens -= amount
                    earnings = amount * -1
                    msg = "Failed."
                elif success >= 49 and success < 97:
                    # Succeeded
                    user_tokens += amount
                    earnings = amount
                    msg = "Success!"
                elif success >= 97 and success <= 100:
                    # Jackpot
                    user_tokens += (amount * 5)
                    earnings = amount * 5
                    msg = "Jackpot!"

                self.bot.gambling_data[str(ctx.author.id)]['tokens'] = user_tokens
                with open('./Data/gambling.json', 'w+') as file:
                    file.write(json.dumps(self.bot.gambling_data, sort_keys = True, indent = 2))

                embed = discord.Embed(
                    title = f"Gambling Results: {msg}",
                    color = self.bot.color
                )
                embed.add_field(
                    name = "Gamble",
                    value = f"`{amount}`"
                )
                embed.add_field(
                    name = "Earned",
                    value = f"`{earnings}`"
                )
                embed.add_field(
                    name = "New Total",
                    value = f"`{user_tokens}`"
                )
                await ctx.send(embed = embed)
            else:
                # User does not have nough coins to bet
                embed = discord.Embed(
                    title = "You do not have that many coins.",
                    description = f"You only have {self.bot.gambling_data[str(ctx.author.id)]['tokens']} coins to bet.",
                    color = self.bot.color
                )
                await ctx.send(embed = embed)
        else:
            # user is not in the data system
            embed = discord.Embed(
                title = f"You have no Coins",
                description = f"To get started earning coins, use `{self.bot.prefix}beg`.",
                color = self.bot.color
            )
            await ctx.send(embed = embed)

    @commands.command(name = "duel", help = "Challenge someone to a betting duel! Winner takes all!", brief = "123 @Heroicos_HM")
    async def duel(self, ctx, amount: int, *, user: discord.User):
        await ctx.trigger_typing()
        if not str(ctx.author.id) in self.bot.gambling_data.keys():
            embed = discord.Embed(
                title = "Denied!",
                description = f"You have no value to duel with. Go `{self.bot.prefix}beg` for more.",
                color = self.bot.color
            )
            await ctx.send(embed = embed)
        elif not str(user.id) in self.bot.gambling_data.keys():
            embed = discord.Embed(
                title = "Well this is sad.",
                description = f"{user.name} has no value to duel with. Tell them to go `{self.bot.prefix}beg` for more.",
                color = self.bot.color
            )
            await ctx.send(embed = embed)
        else:
            if self.bot.gambling_data[str(ctx.author.id)]['tokens'] < amount:
                embed = discord.Embed(
                    title = "Denied!",
                    description = f"You do not have enough coins to duel with that amount. Go `{self.bot.prefix}beg` for more.",
                    color = self.bot.color
                )
                embed.add_field(
                    name = f"Your Coins",
                    value = f"{self.bot.gambling_data[str(ctx.author.id)]['tokens']} Coins"
                )
                await ctx.send(embed = embed)
            elif self.bot.gambling_data[str(user.id)]['tokens'] < amount:
                embed = discord.Embed(
                    title = "Well this is sad.",
                    description = f"{user.name} does not have enough coins to duel with that amount. Tell them to go `{self.bot.prefix}beg` for more.",
                    color = self.bot.color
                )
                embed.add_field(
                    name = f"{user.name}'s Coins",
                    value = f"{self.bot.gambling_data[str(user.id)]['tokens']} Coins"
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = f"{ctx.author.name} Challenges You!",
                    description = f"{ctx.author.mention} has challenged you to a gambling duel. Winner takes all. You have 2 minutes to click the :white_check_mark: reaction below to accept.",
                    color = self.bot.color
                )
                embed.add_field(
                    name = f"{ctx.author.name}'s Coins'",
                    value = self.bot.gambling_data[str(ctx.author.id)]['tokens']
                )
                embed.add_field(
                    name = f"{user.name}'s Coins'",
                    value = self.bot.gambling_data[str(user.id)]['tokens']
                )
                embed.add_field(
                    name = "Entry Fee",
                    value = f"`{amount}`"
                )
                embed.add_field(
                    name = "Prize Pool",
                    value = f"`{amount * 2}`"
                )
                msg = await ctx.send(embed = embed, content = user.mention)
                await msg.add_reaction('✅')

                def check(reaction, reactor):
                    return reactor == user and str(reaction.emoji == '✅') and reaction.message.id == msg.id

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                except asyncio.TimeoutError:
                    await msg.delete()
                else:
                    entrants = [ctx.author, user]
                    winner = random.choice(entrants)
                    entrants.remove(winner)

                    user_tokens = self.bot.gambling_data[str(winner.id)]['tokens'] + amount
                    self.bot.gambling_data[str(winner.id)]['tokens'] = user_tokens
                    for loser in entrants:
                        loser_tokens = self.bot.gambling_data[str(loser.id)]['tokens'] - amount
                        self.bot.gambling_data[str(loser.id)]['tokens'] = loser_tokens
                    with open('./Data/gambling.json', 'w+') as file:
                        file.write(json.dumps(self.bot.gambling_data, sort_keys = True, indent = 2))
                    embed = discord.Embed(
                        title = f"{winner.name} Wins!",
                        color = self.bot.color
                    )
                    embed.add_field(
                        name = "Winnings",
                        value = f"`{amount}`"
                    )
                    embed.add_field(
                        name = "New Total",
                        value = f"`{user_tokens}`"
                    )
                    await msg.edit(embed = embed, content = None)

def setup(bot):
    bot.add_cog(Gambling(bot))
