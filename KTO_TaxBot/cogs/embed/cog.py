from discord import Embed
from discord.ext import commands
from typing import Optional
import logging
import serverconfig

class CustomEmbed(commands.Cog):
    """Provides methods to build and return fully formed custom embeds."""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.embed")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("embed cog initialised")

    async def newembed(ctx, title: str, type: Optional[str]="rich", description: Optional[str]=None, fields: Optional[list[dict]]=None, footer: Optional[str]=None, server_id: Optional[int]=None):
        """Constructs and returns a new embed."""
        if server_id == None:
            server_id = ctx.guild.id
        embed = Embed(
            type = type,
            title = title,
            description = description,
            color=serverconfig.configuration[server_id]["colour_id"]
        )
        if fields != None:
            for field in fields:
                embed.add_field(
                    name = field["name"],
                    value = field["value"],
                    inline = field["inline"]
                )
        if fields != None:
            embed.set_footer(
                text=footer
            )
        return embed

def setup(bot: commands.Bot):
    bot.add_cog(CustomEmbed(bot))
