from asyncio.log import logger
from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions
import logging

class Ping(commands.Cog):
    """Receives ping commands"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.ping")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("ping cog initialised")

    @slash_command()
    @has_permissions(administrator=True)
    async def ping(self, ctx):
        """Tests bot connectivity by responding with \'Pong\' if online."""
        logger.info("Sending 'Pong'...")
        await ctx.respond("Pong")

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
