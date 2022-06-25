from discord import Option
from discord.commands import slash_command
from discord.ext import commands
from typing import Optional
from discord.ext.commands import has_permissions
import logging
from ..embed.cog import CustomEmbed

class CustomHelp(commands.Cog):
    """Provides help informaion about the bot"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.help")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("help cog initialised")

    @slash_command()
    @has_permissions(administrator=True)
    async def help(self, ctx, command: Option(str, 'Pick a command to learn more about.', required=False, choices=['help','ping','resetconfig','setcolour','setembedchannel','setlogchannel','showconfig'])):
        """Displays help text for a command, or general help if no command is specified."""
        fields = []
        match command:
            case None:
                fields.append({"name": "/help", "value": "Displays help information for the bot.", "inline": False})
                fields.append({"name": "/ping", "value": "Responds with 'Pong' if online.", "inline": False})
                fields.append({"name": "/resetconfig", "value": "Reset the bot's configuration to default.", "inline": False})
                fields.append({"name": "/setcolour", "value": "Set the colour for the bot to use.", "inline": False})
                fields.append({"name": "/setlogchannel", "value": "Set the channel where the bot logs to.", "inline": False})
                fields.append({"name": "/showconfig", "value": "Shows the bot's current configuration.", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP", description="See below for available commands.", fields=fields)
                embedinvisible = False
            case "help":
                fields.append({"name": "Usage", "value": "/help\n/help command:(OPTION)", "inline": False})
                fields.append({"name": "Options - command", "value": "help\nping\nsetcolour\nsetembedchannel\nsetlogchannel\nsetupdatechannel\nshowconfig", "inline": False})
                fields.append({"name": "Returns", "value": "An embed displaying the requested help content.", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - HELP", description="Use this command to see general help information or help information for a specific command.", fields=fields)
                embedinvisible = False
            case "ping":
                fields.append({"name": "Usage", "value": "/ping", "inline": False})
                fields.append({"name": "Options", "value": "None", "inline": False})
                fields.append({"name": "Returns", "value": "Pong", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - PING", description="Use this command to check if the bot is online and responsive.", fields=fields)
                embedinvisible = False
            case "resetconfig":
                fields.append({"name": "Usage", "value": "/resetconfig config:(OPTION)", "inline": False})
                fields.append({"name": "Options - config", "value": "**all** : Resets all config to default / off\n**colour** : Resets the Bot's colour to default\n**embed_channel** : Bot will remove and stop updating the dynamic embed\n**log_channel** : Bot will stop logging\n**update_channel** : Bot will stop posting OpenSea updates", "inline": False})
                fields.append({"name": "Returns", "value": "An embed confirming that the configuration has been reset.", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - RESETCONFIG", description="Use this command to reset the bot's configuration to default.", fields=fields)
                embedinvisible = False
            case "setcolour":
                fields.append({"name": "Usage", "value": "/setcolour colour:(OPTION)", "inline": False})
                fields.append({"name": "Options - colour (Pick from 24 colours)", "value": "AQUA\nBLACK\nBLUE\nBLURPLE\nDARK_AQUA\nDARK_BLUE\nDARK_GOLD\nDARK_GREEN\nDARK_GREY\nDARK_ORANGE\nDARK_PURPLE\nDARK_RED\nFUSCHIA\nGOLD\nGREEN\nGREY\nGREYPLE\nLIGHT_GREY\nNAVY\nORANGE\nPURPLE\nRED\nWHITE\nYELLOW\n", "inline": False})
                fields.append({"name": "Returns", "value": "An embed confirming that the colour has been updated.", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - SETCOLOUR", description="Use this command to set a colour for the bot to use.", fields=fields)
                embedinvisible = False
            case "setlogchannel":
                fields.append({"name": "Usage", "value": "/setembedchannel channel:(OPTION)", "inline": False})
                fields.append({"name": "Options", "value": "Any text channel in your server", "inline": False})
                fields.append({"name": "Returns", "value": "An embed confirming that the log channel has been updated", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - SETLOGCHANNEL", description="Use this command to set the channel for the bot to log to.", fields=fields)
                embedinvisible = False
            case "showconfig":
                fields.append({"name": "Usage", "value": "/showconfig", "inline": False})
                fields.append({"name": "Options", "value": "None", "inline": False})
                fields.append({"name": "Returns", "value": "An embed showing the bot's current configuration.", "inline": False})
                helpembed = await CustomEmbed.newembed(ctx, title="HELP - SHOWCONFIG", description="Use this command to display the current bot configuration for your server.", fields=fields)
                embedinvisible = False
            case _:
                helpembed = await CustomEmbed.newembed(ctx, title="Error!", description="That is not an available command!")
                embedinvisible = True
        logger.info("Sending help embed...")
        await ctx.respond(embed = helpembed, ephemeral = embedinvisible)

def setup(bot: commands.Bot):
    bot.add_cog(CustomHelp(bot))
