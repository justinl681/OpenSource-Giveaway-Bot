import discord
import random
import datetime
import asyncio
from discord.ext import commands
import time


bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    game = discord.Game("responding to $ghelp!")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embedVar = discord.Embed(title="Helping you out!", description="The correct way to start a giveaway is '$new (prize for the giveaway), (time to claim the prize in minutes)' or for the reroll command: '$reroll (message id of the giveaway you want to reroll)'", color=0x00ff00)
        embedVar.add_field(name="Sidenote:", value="If you're having trouble with multiple-word prizes, use periods (.) instead of spaces.")
        await ctx.send(embed=embedVar)  


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def new(ctx, prize, mins: int):
    end = datetime.datetime.utcnow().replace(microsecond=0) + datetime.timedelta(minutes=mins)
    embedVar = discord.Embed(title="New Giveaway!", description=prize.replace('.', ' '), color=0x00ff00)
    embedVar.add_field(name= "Ends at:", value=end)
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🎉")
    await asyncio.sleep(mins*60)
    mesg = await ctx.fetch_message(msg.id)
    users = await mesg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)
    await ctx.send(f"{winner.mention} won {prize.replace('.', ' ')}")
    embedVar = discord.Embed(title=f"{winner.name} won:", description=prize.replace('.', ' '), color=0x00ff00)
    await mesg.edit(embed=embedVar)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def reroll(ctx, messageid):
    mesg = await ctx.fetch_message(messageid)
    users = await mesg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)
    embedVar = discord.Embed(title=f"Reroll!", description=f"{winner.name} won!")
    await ctx.send(embed=embedVar)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ghelp(ctx):
    embedVar = discord.Embed(title="Helping you out!", description="The correct way to start a giveaway is '$new (prize for the giveaway), (time to claim the prize in minutes)' or for the reroll command: '$reroll (message id of the giveaway you want to reroll)'", color=0xfffff)
    embedVar.add_field(name="Sidenote:", value="If you're having trouble with multiple-word prizes, use periods (.) instead of spaces.")
    await ctx.send(embed=embedVar)

bot.run('token')
