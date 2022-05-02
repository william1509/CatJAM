from discord import Client
import os
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("Token not found")
    exit(1)

bot = Client()
slash = SlashCommand(bot, sync_commands=True)

@bot.command(name="test") # Test command which works
async def test(ctx):
    await ctx.send("test")

# @slash.slash(name="test", guild_ids=[934657083922587658])
# async def test(ctx: SlashContext):
#     await ctx.send("test")

bot.run(TOKEN)