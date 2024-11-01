import asyncio
import os
import discord
import youtube_dl
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

load_dotenv()

TOKEN = os.getenv('DISCORD_CAT_JAM_TOKEN')
if TOKEN is None:
    print("Token not found")
    exit(1)


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_results = []
        self.queue = []

    @commands.command()
    async def summon(self, ctx):
        """Joins a voice channel"""
        channel = ctx.author.voice.channel
        if channel:
            return await ctx.voice_client.move_to(channel)
        
        await ctx.send("You need to be in a voice channel")
    
    @commands.command()
    async def search(self, ctx, keywords: str = None):
        if keywords is None:
            await ctx.send('You need to enter some keywords')
            return
        
        video_search: VideosSearch = VideosSearch(keywords, limit=5)
        self.search_results = video_search.result()["result"]
        choices = [f"{i} - {res['title']}" for (i, res) in enumerate(self.search_results, start=1)]
        await ctx.send("\n".join(choices))

    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        if url.isdigit():
            video_id = self.search_results[int(url) - 1]['id']
            player = await YTDLSource.from_url(f'https://www.youtube.com/watch?v={video_id}', loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def kill(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @summon.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))
bot.run(TOKEN)
