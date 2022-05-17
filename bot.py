import os
from dotenv import load_dotenv
import interactions
from youtubesearchpython import VideosSearch

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("Token not found")
    exit(1)


bot = interactions.Client(token=TOKEN)

@bot.command(
    name="search",
    description="Displays a list of songs from youtube",
    scope=305408270083031040,
    options = [
        interactions.Option(
            name="keywords",
            description="Enter some keywords to help me find your song",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],

)
async def search(ctx: interactions.CommandContext, keywords: str):
    video_search: VideosSearch = VideosSearch(keywords, limit=5)
    message = [f"{i} - {res['title']}" for (i, res) in enumerate(video_search.result()["result"], start=1)]
    await ctx.send("\n".join(message))

bot.start()