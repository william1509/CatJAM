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

# @bot.command(
#     name="search",
#     description="Displays a list of songs from youtube",
#     scope=305408270083031040,
#     options = [
#         interactions.Option(
#             name="Keywords",
#             description="Enter some keywords to help me find your song",
#             type=interactions.OptionType.STRING,
#             required=True,
#         ),
#     ],

# )
# async def play(ctx, keywords: str):
#     results = VideosSearch(keywords, limit=5)
#     await ctx.send(f"you said {text}")
button = interactions.SelectMenu (
    style=3,
    label="hello world!",
    custom_id="hello",
    options=[interactions.SelectOption(
            label="I'm a cool option. :)",
            value="internal_option_value",
            description="some extra info about me! :D")
            ]
)

@bot.command(
    name="button_test",
    description="This is the first command I made!",
    scope=305408270083031040,
)
async def button_test(ctx):
    await ctx.send("testing", components=button)

@bot.component("hello")
async def button_response(ctx, text: interactions.SelectOption):
    await ctx.send(f"You clicked the Button {text}", ephemeral=True)

bot.start()


bot.start()