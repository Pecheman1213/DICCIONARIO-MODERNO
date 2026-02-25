import discord
from bot_logic import flip_coin 
from discord.ext import commands

# Prefijo del bot
intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(command_prefix="!p ", intents=intents)

@bot.command(name = "saludar")
async def saludar(ctx):
    await ctx.send("Hola")


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


bot.run(")
