import os
import discord
from pathlib import Path
from discord import user
from discord.ext import tasks
from discord import Intents, Guild
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from dotenv import load_dotenv
from services import kounotori

cwd = Path(__file__).parents[0]
cwd = str(cwd)
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
print("Bot is loading, please wait...")
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix="!", help_command=None, intents=Intents.all())
slash = SlashCommand(bot, sync_commands=False)

class Slash():
    def __init__(self, bot: Bot):
        self.bot = bot



@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="KTO Price (USD)"))
    
    
if __name__ == '__main__':
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)
