
from discord.ext.commands import Bot, Cog
from discord.ext import tasks
from discord import Intents, Guild
from services import kounotori

OLD_PRICE = None

class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Commands Cog loaded.")

    @tasks.loop(seconds=60)
    async def change_status(self):
        global OLD_PRICE
        TokenPrice = await kounotori.getPrice()
        if TokenPrice != OLD_PRICE:
            print(f"Price has just updated ${TokenPrice}")
            guild = self.bot.get_guild(893600091686981722)
            namechange = guild.get_member(user_id=885604289265930250)
            await namechange.edit(nick=TokenPrice)
            OLD_PRICE = TokenPrice
        else:
            print(f"Price hasn't been updated")

def setup(bot):
    bot.add_cog(Commands(bot))
