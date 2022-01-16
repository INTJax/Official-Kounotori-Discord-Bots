import os
from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from discord import Intents, Guild
from services import kounotori

OLD_HOLDERS = None

class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Commands Cog loaded.")

    @tasks.loop(seconds=10)
    async def change_status(self):
        global OLD_HOLDERS
        TokenHolders = await kounotori.getHolders()
        if TokenHolders != OLD_HOLDERS:
            print(f"Number of holders has just changed ${TokenHolders}")
            guild = self.bot.get_guild(893600091686981722)
            namechange = guild.get_member(user_id=921725166558527538)
            await namechange.edit(nick=TokenHolders)
            OLD_HOLDERS = TokenHolders
        else:
            print(f"Number of holders hasn't changed")

def setup(bot):
    bot.add_cog(Commands(bot))
