from asyncio.log import logger
from discord.ext import commands, tasks
from discord.ext.commands import Cog
import os
import logging
import serverconfig

class Burn(commands.Cog):
    """Keeps track of and updates it's nickname to the KTO burn total"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.burn")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("burn cog initialised")
    
    #Set variables required for supply updates
    global OldAmount
    OldAmount = "0"
    global DataSource
    DataSource = os.getenv("KTO_DATA")
    logger.debug(f"DataSource is: {DataSource}")

    @Cog.listener()
    async def on_ready(self):
        self.updatevalue.start()

    #Function to retrieve the required KTO data
    async def getKTOData():
        logger.debug("Getting KTO data...")
        global DataSource
        logger.debug(f"DataSource is: {DataSource}")
        try:
            with open(DataSource) as f:
                KTOData = f.readline().rstrip()
                f.close()
                return KTOData
        except Exception as e:
            logger.error(f"There was an error reading burn data! Error was: {e}")

    #Function to update the nickname on all servers
    async def updateNickname(ctx, Amount):
        logger.info("Updating ALL nicknames to %s", Amount)
        for server_id in serverconfig.configuration:
            if serverconfig.configuration[server_id] != None:
                DiscGuild = ctx.bot.get_guild(server_id)
                await (DiscGuild.get_member(ctx.bot.user.id)).edit(nick=Amount)
                logger.debug("Updated nickname for server %s", DiscGuild)
        logger.info("Updated ALL nicknames")

    #Function to update the nickname on one server (to ensure new servers perform a quick initial update)
    async def updateOneNickname(ctx, Amount, DiscGuild):
        logger.info("Updating nickname on %s", DiscGuild)
        await (DiscGuild.get_member(ctx.bot.user.id)).edit(nick=Amount)
        logger.info("Updated nickname to %s", Amount)

    #Function to check that the nickname in all servers is set appropriately
    async def checkNickname(ctx, Amount):
        logger.debug("Checking nicknames on ALL servers")
        for server_id in serverconfig.configuration:
            if serverconfig.configuration[server_id] != None:
                DiscGuild = ctx.bot.get_guild(server_id)
                CurrentNick = (DiscGuild.get_member(ctx.bot.user.id)).nick
                if CurrentNick != Amount:
                    logger.info("Nickname in server %s is not correct", DiscGuild)
                    await Burn.updateOneNickname(ctx, Amount, DiscGuild)

    #Main function that controls the frequency of retrieving data and updating nicknames
    @tasks.loop(seconds=10)
    async def updatevalue(ctx):
        logger.info("Checking for new burn...")
        global OldAmount
        Amount = await Burn.getKTOData()
        if Amount != OldAmount:
            logger.info("Amount has changed to %s", Amount)
            await Burn.updateNickname(ctx, Amount)
            OldAmount = Amount
        else:
            logger.info("Amount has not changed")
            await Burn.checkNickname(ctx, Amount)

def setup(bot: commands.Bot):
    bot.add_cog(Burn(bot))
