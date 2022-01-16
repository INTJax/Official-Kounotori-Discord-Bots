import os
import discord
from pathlib import Path
from discord import user
from discord.ext import tasks, commands
from discord import Intents, Guild
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv
from services import kounotori

cwd = Path(__file__).parents[0]
cwd = str(cwd)
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
print("Bot is loading, please wait...")
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix="!", help_command=None, intents=None)
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(
    name="tax",
    description="Returns a breakdown of current KTO tax rates.",
    guild_ids=[893600091686981722]
)
async def _tax(ctx:SlashContext):
    with open('//DOMCON_1/KTO_Data/Tax_Details/BuyMTax.txt') as f:
                BuyMTax = f.readline().rstrip()
    with open('//DOMCON_1/KTO_Data/Tax_Details/BuyReflect.txt') as f:
                BuyReflect = f.readline().rstrip()
    with open('//DOMCON_1/KTO_Data/Tax_Details/SellMTax.txt') as f:
                SellMTax = f.readline().rstrip()
    with open('//DOMCON_1/KTO_Data/Tax_Details/SellReflect.txt') as f:
                SellReflect = f.readline().rstrip()
    with open('//DOMCON_1/KTO_Data/Tax_Details/TferMtax.txt') as f:
                TferMtax = f.readline().rstrip()
    with open('//DOMCON_1/KTO_Data/Tax_Details/TferReflect.txt') as f:
                TferReflect = f.readline().rstrip()
    TaxDetail = discord.Embed(
        title="KTO Tax Breakdown",
        description="",
        color=0xff7573
    )
    TaxDetail.add_field(
        name="Buy Tax:",
        value="Reflections: " + BuyReflect + "\nMarketing: " + BuyMTax,
        inline=False
    )
    TaxDetail.add_field(
        name="Sell Tax:",
        value="Reflections: " + SellReflect + "\nMarketing: " + SellMTax,
        inline=False
    )
    TaxDetail.add_field(
        name="Transfer Tax:",
        value="Reflections: " + TferReflect + "\nMarketing: " + TferMtax,
        inline=False
    )
    TaxDetail.set_footer(
        text="Requested by: {}".format(ctx.author.display_name)
    )
    await ctx.send(embed=TaxDetail)

class Slash():
    def __init__(self, bot: Bot):
        self.bot = bot

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="KTO Tax Rate"))

if __name__ == '__main__':
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)
