import logging
import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.commands import has_permissions
import serverconfig
from ..embed.cog import CustomEmbed

class Configuration(commands.Cog):
    """Contains functions to read and write config per server"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.config")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("config cog initialised")
    
    async def save_config():
        """Writes the current configuration in memory to the configuration file"""
        with open("serverconfig.py", "w") as config_file:
            config_file.write(f"configuration = {serverconfig.configuration}")
            config_file.close()

    async def new_config(server_id):
        """Saves a new set of server config to the config file as a placeholder"""
        serverconfig.configuration[server_id] = {"embed_channel": None, "embed_channel_id": None, "log_channel": None, "log_channel_id": None, "colour": "BLURPLE", "colour_id": 5793266}
        await Configuration.save_config()

    async def delete_config(server_id):
        """Removed a set of server config from the config file"""
        if server_id in serverconfig.configuration:
            del serverconfig.configuration[server_id]
            await Configuration.save_config()

    async def update_config(server_id, config_id, config_value):
        """Updates one particular value in a server's configuration data"""
        if server_id not in serverconfig.configuration:
            await Configuration.new_config(server_id)
        serverconfig.configuration[server_id][config_id] = config_value
        await Configuration.save_config()

    @slash_command()
    @has_permissions(administrator=True)
    async def resetconfig(self, ctx, config: Option(str, 'Pick a config value to reset, or rest all config', required=True, choices=['all','colour','embed_channel','log_channel'])):
        """Reset the bot's configuration to default"""
        server_id = ctx.guild.id
        match config:
            case 'all':
                await Configuration.delete_config(server_id)
                await Configuration.new_config(server_id)
                embed = await CustomEmbed.newembed(ctx, title="All configuration has been reset!")
            case 'colour':
                await Configuration.update_config(server_id, "colour", "BLURPLE")
                await Configuration.update_config(server_id, "colour_id", 5793266)
                embed = await CustomEmbed.newembed(ctx, title="Configuration for colour has been reset!")
            case 'embed_channel':
                await Configuration.update_config(server_id, "embed_channel", None)
                await Configuration.update_config(server_id, "embed_channel_id", None)
                embed = await CustomEmbed.newembed(ctx, title="Configuration for embed_channel has been reset!")
            case 'log_channel':
                await Configuration.update_config(server_id, "log_channel", None)
                await Configuration.update_config(server_id, "log_channel_id", None)
                embed = await CustomEmbed.newembed(ctx, title="Configuration for log_channel has been reset!")
        await ctx.respond(embed=embed)

    @slash_command()
    @has_permissions(administrator=True)
    async def showconfig(self, ctx):
        """Displays the bot's current configuration"""
        server_id = ctx.guild.id
        fields = []
        if server_id not in serverconfig.configuration:
            await Configuration.new_config(server_id)
        for key in serverconfig.configuration[server_id]:
            if "_id" not in key:
                fields.append({"name": key, "value": f"{serverconfig.configuration[server_id][key]}", "inline": False})
        embed = await CustomEmbed.newembed(ctx, title="CONFIGURATION", description="See below for current configuration values.", fields=fields)
        await ctx.respond(embed=embed)

    @slash_command()
    @has_permissions(administrator=True)
    async def setembedchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel where the buy embeds are posted"""
        logger.debug("Beginning setembedchannel function")
        server_id = ctx.guild.id
        embed_channel = (channel.name).encode("ascii", "ignore")
        embed_channel = embed_channel.decode()
        embed_channel_id = channel.id
        await Configuration.update_config(server_id, "embed_channel", embed_channel)
        logger.debug("Config embed_channel updated")
        await Configuration.update_config(server_id, "embed_channel_id", embed_channel_id)
        logger.debug("Config embed_channel_id updated")
        embed = await CustomEmbed.newembed(ctx, title=f"The embed channel has been set to {embed_channel}!")
        await ctx.respond(embed=embed)

    @slash_command()
    @has_permissions(administrator=True)
    async def setlogchannel(self, ctx, channel: discord.TextChannel):
        """Set the channel where the bot logs to"""
        server_id = ctx.guild.id
        log_channel = (channel.name).encode("ascii", "ignore")
        log_channel = log_channel.decode()
        log_channel_id = channel.id
        await Configuration.update_config(server_id, "log_channel", log_channel)
        await Configuration.update_config(server_id, "log_channel_id", log_channel_id)
        embed = await CustomEmbed.newembed(ctx, title=f"The log channel has been set to {log_channel}!")
        await ctx.respond(embed=embed)

    @slash_command()
    @has_permissions(administrator=True)
    async def setcolour(self, ctx, colour: Option(str, 'Pick a colour for the bot to use', required=True, choices=['AQUA','BLACK','BLUE','BLURPLE','DARK_AQUA','DARK_BLUE','DARK_GOLD','DARK_GREEN','DARK_GREY','DARK_ORANGE','DARK_PURPLE','DARK_RED','FUSCHIA','GOLD','GREEN','GREY','GREYPLE','LIGHT_GREY','NAVY','ORANGE','PURPLE','RED','WHITE','YELLOW'])):
        match colour:
            case 'AQUA':
                colour_id = 1752220
            case 'BLACK':
                colour_id = 2303786
            case 'BLUE':
                colour_id = 3447003
            case 'BLURPLE':
                colour_id = 5793266
            case 'DARK_AQUA':
                colour_id = 1146986
            case 'DARK_BLUE':
                colour_id = 2123412
            #case 'DARK_BUT_NOT_BLACK':
                #colour_id = 2895667
            case 'DARK_GOLD':
                colour_id = 12745742
            case 'DARK_GREEN':
                colour_id = 2067276
            case 'DARK_GREY':
                colour_id = 9936031
            #case 'DARK_NAVY':
                #colour_id = 2899536
            case 'DARK_ORANGE':
                colour_id = 11027200
            case 'DARK_PURPLE':
                colour_id = 7419530
            case 'DARK_RED':
                colour_id = 10038562
            #case 'DARK_VIVID_PINK':
                #colour_id = 11342935
            #case 'DARKER_GREY':
                #colour_id = 8359053
            case 'FUSCHIA':
                colour_id = 15418782
            case 'GOLD':
                colour_id = 15844367
            case 'GREEN':
                colour_id = 5763719
            case 'GREY':
                colour_id = 9807270
            case 'GREYPLE':
                colour_id = 10070709
            case 'LIGHT_GREY':
                colour_id = 12370112
            #case 'LUMINOUS_VIVID_PINK':
                #colour_id = 15277667
            case 'NAVY':
                colour_id = 3426654
            #case 'NOT_QUITE_BLACK':
                #colour_id = 2303786
            case 'ORANGE':
                colour_id = 15105570
            case 'PURPLE':
                colour_id = 10181046
            case 'RED':
                colour_id = 15548997
            case 'WHITE':
                colour_id = 16777215
            case 'YELLOW':
                colour_id = 16705372
            case _:
                colour_id = 10070709
        server_id = ctx.guild.id
        await Configuration.update_config(server_id, "colour", colour)
        await Configuration.update_config(server_id, "colour_id", colour_id)
        embed = await CustomEmbed.newembed(ctx, title=f"The Bot's colour has been set to {colour}!")
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Configuration(bot))
