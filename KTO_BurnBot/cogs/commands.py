import os
from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from discord import Intents, Guild
from services import kounotori

OLD_Amount = None

class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Commands Cog loaded.")

    @tasks.loop(seconds=10)
    async def change_status(self):
        global OLD_Amount
        Amount = await kounotori.getBurntKTO()
        if Amount != OLD_Amount:
            print(f"Number of burnt tokens has changed ${Amount}")
            guild = self.bot.get_guild(893600091686981722)
            namechange = guild.get_member(user_id=922019937902542858)
            await namechange.edit(nick=Amount)
            OLD_Amount = Amount
        else:
            print(f"Amount hasn't changed")

def setup(bot):
    bot.add_cog(Commands(bot))
