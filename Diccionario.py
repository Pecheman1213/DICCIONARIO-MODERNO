import discord
from bot_logic import flip_coin 
from bot_logic import get_duck_image_url
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import random

# Prefijo del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
 
bot = commands.Bot(command_prefix="!p ", intents=intents)


@bot.event
async def on_ready():

    print(f"Bot conectado como {bot.user}")


ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            data = data['entries'][0]
        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data)


@bot.command(name = "saludar")
async def saludar(ctx):
    await ctx.send(f"Hola {ctx.author.mention}")


repetir = True

@bot.command()
async def repeat(ctx, times: int, content='rena te meo'):
    global repetir
    repetir = True
    for i in range(times):
        if not repetir:
            break
        await ctx.send(content)
        await asyncio.sleep(1)

@bot.command()
async def parar(ctx):
    global repetir
    repetir = False
    await ctx.send("Listo bro, pare de decir factous")

@bot.command()
async def sonidito(ctx):
    if ctx.author.voice is None:
        await ctx.send("no estas en ningun canal de voz hermanito")
        return

    vc = await ctx.author.voice.channel.connect()
    player = await YTDLSource.from_url("https://www.youtube.com/watch?v=nXM2hDK7_Dc", loop=bot.loop)
    vc.play(player)

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()


@bot.command()
async def sonidito2(ctx):
    if ctx.author.voice is None:
        await ctx.send("no estas en ningun canal de voz hermanito")
        return

    vc = await ctx.author.voice.channel.connect()
    player = await YTDLSource.from_url("https://www.youtube.com/watch?v=0NAgfjQNJwg", loop=bot.loop)
    vc.play(player)

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()

@bot.command()
async def BASTA(ctx):
    if ctx.voice_client is None:
        await ctx.send("no estas en ningun canal de voz hermanito")
        return
    await ctx.voice_client.disconnect()


@bot.command()
async def panchito(ctx):
    imagenes = ['images/panchulo.jpeg', 'images/panchulo2.png', 'images/panchulo3.png']
    imagen = random.choice(imagenes)
    with open(imagen, 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)


@bot.command('duck')

async def duck(ctx):

    '''Una vez que llamamos al comando duck, 

    el programa llama a la función get_duck_image_url'''

    image_url = get_duck_image_url()

    await ctx.send(image_url)


bot.run(")
