import discord
from bot_logic import flip_coin 
from bot_logic import get_duck_image_url
from bot_logic import get_partidos
from bot_logic import get_tabla
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import random


API_KEY = "c15cbde00ae5492898f29c7197cd8beb"

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

@bot.command()
async def partidos(ctx, liga="PL"):
    lista = get_partidos(liga)
    if not lista:
        await ctx.send("No hay partidos!")
        return
    
    mensaje = f"**Partidos de {liga}:**\n"
    for p in lista[:5]:
        local = p['homeTeam']['name']
        visita = p['awayTeam']['name']
        hora = p['utcDate'][11:16]
        marcador = f"{p['score']['fullTime']['home']} - {p['score']['fullTime']['away']}"
        mensaje += f"⚽ {local} {marcador} {visita} - {hora} UTC\n"
    
    await ctx.send(mensaje)


@bot.command()
async def tabla(ctx, liga="PL"):
    standings = get_tabla(liga)
    if not standings:
        await ctx.send("No encontré la tabla!")
        return
    
    mensaje = f"**Tabla de {liga}:**\n"
    for equipo in standings[:10]:
        pos = equipo['position']
        nombre = equipo['team']['name']
        pts = equipo['points']
        mensaje += f"{pos}. {nombre} - {pts} pts\n"
    
    await ctx.send(mensaje)

@bot.command()
async def ayuda(ctx):
    mensaje = """**Ligas disponibles:**
🏴󠁧󠁢󠁥󠁮󠁧󠁿 `PL` — Premier League
🇪🇸 `PD` — La Liga
🇮🇹 `SA` — Serie A
🇩🇪 `BL1` — Bundesliga
🇫🇷 `FL1` — Ligue 1
🇪🇺 `CL` — Champions League
🇪🇺 `EL` — Europa League
🇪🇺 `EC` — Eurocopa
🌍 `WC` — Mundial
🇧🇷 `BSA` — Serie A Brasil
🇵🇹 `PPL` — Primeira Liga
🇳🇱 `DED` — Eredivisie

**Comandos:**
`!p partidos [liga]` — partidos de hoy
`!p tabla [liga]` — tabla de posiciones
`!p prediccion [equipo1] [equipo2]` — predice el resultado de un partido"""
    await ctx.send(mensaje)

@bot.command()
async def prediccion(ctx, equipo1, equipo2):
    goles1 = random.randint(0, 5)
    goles2 = random.randint(0, 5)
    
    if goles1 > goles2:
        resultado = f"🏆 Gana {equipo1}!"
    elif goles2 > goles1:
        resultado = f"🏆 Gana {equipo2}!"
    else:
        resultado = "🤝 Empate!"
    
    await ctx.send(f"**Predicción:**\n⚽ {equipo1} {goles1} - {goles2} {equipo2}\n{resultado}")


bot.run(")
