import discord # Library of the API discord.py
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.is_playing = False #Variable to know if a song is playing 

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

@commands.command(name="join", help="Join the bot to the current channel")
async def join(self, ctx):
      print("!join")
      if ctx.author.voice is None:
          await ctx.send("Primero necesitas estar en un canal de voz, amigo mío.")
      voice_channel = ctx.author.voice.voice_channel
      if ctx.voice_client is None:
        await voice_channel.connect()
      else:
        await ctx.voice_client.move_to(voice_channel)

@commands.command(name="disconnect", help="Disconnects the bot from the channel")
async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()

@commands.command(name="pause", help="Pause the song")
async def pause(self, ctx):
  if self.is_playing:
    await ctx.voice_client.pause()
    await ctx.send("Música pausada, mi rey 😎🤙")
  else:
    await ctx.send("No hay musica bro 🤙")
    
@commands.command(name="resume", help="Resume the song")
async def resume(self, ctx):
  if not self.is_playing:
    await ctx.voice_client.resume()
    await ctx.send("Música reproduciéndose 😎🎶")
  else:
    await ctx.send("No hay musica bro 🤙")

@commands.command(name="skip", help="Skips the current song being played")
async def skip(self, ctx):
    if self.vc != "" and self.vc:
        self.vc.stop()
        #try to play next in the queue if it exists
        await self.play_music()

@commands.command(name="play", help="Plays a selected song from youtube")
async def play(self, ctx, *args):
    query = " ".join(args)
        
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        #you need to be connected so that the bot knows where to go
        await ctx.send("Conectaisimo")
    else:
        song = self.search_yt(query)
        if type(song) == type(True):
            await ctx.send("Chaval que la cancion no la he ecnontrado, soy un maquina pero no tanto")
        else:
            await ctx.send("Cheeeeee, añadia")
            self.music_queue.append([song, voice_channel])
            
            if self.is_playing == False:
                await self.play_music()

# infinite loop checking 
async def play_music(self):
    if len(self.music_queue) > 0:
        self.is_playing = True

        m_url = self.music_queue[0][0]['source']
        
        #try to connect to voice channel if you are not already connected

        if self.vc == "" or not self.vc.is_connected() or self.vc == None:
            self.vc = await self.music_queue[0][1].connect()
        else:
            await self.vc.move_to(self.music_queue[0][1])
        
        print(self.music_queue)
        #remove the first element as you are currently playing it
        self.music_queue.pop(0)

        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
        self.is_playing = False

#searching the item on youtube
def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
        try: 
            info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
        except Exception: 
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}

def play_next(self):
    if len(self.music_queue) > 0:
        self.is_playing = True

        #get the first url
        m_url = self.music_queue[0][0]['source']

        #remove the first element as you are currently playing it
        self.music_queue.pop(0)

        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
        self.is_playing = False