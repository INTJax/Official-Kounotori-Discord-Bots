import os
import discord
import logging
from logging import *
from dotenv import load_dotenv
from discord.ext.commands import Bot
from cogs.config.cog import Configuration
import serverconfig

def main():
    # Configure bot logging
    logger = logging.getLogger("discord.bot")
    logger.info("******************** STARTING NEW INSTANCE ********************")
    print(f"LOG_LEVEL = {log_level}, LOG_MODE = {log_mode}")
    logger.info(f"LOG LEVEL = '{log_level}', LOG MODE = '{log_mode}'")

    #Set bot description
    Description = 'Official KTO Holders Bot'

    # Set up required intents
    intents = discord.Intents.default()
    #intents.members = True
    #intents.guilds = True

    #Set activity variables
    ActivityType = discord.ActivityType.watching
    ActivityName = 'KTO Holders'
    Activity = discord.Activity(type=ActivityType, name=ActivityName)

    # Initialise the bot
    client = Bot(command_prefix='$', description=Description, intents = intents, help_command = None)

    # Load all cogs
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            client.load_extension(f"cogs.{folder}.cog")
    logger.info("Cogs loaded.")

    # Define events for the bot to listen for
    ###########################################

    # Bot ready
    @client.event
    async def on_ready():
        await client.wait_until_ready()
        print(f"{client.user.name} has connected to Discord.")
        logger.info(f"{client.user.name} has connected to Discord.")
        print(f"Server configuration is: {serverconfig.configuration}")
        logger.debug(f"Server configuration is: {serverconfig.configuration}")
        await client.change_presence(activity = Activity)

    # Bot joins a server
    @client.event
    async def on_guild_join(guild):
        await Configuration.new_config(guild.id)

    # Bot leaves a server (kicked / banned etc.)
    @client.event
    async def on_guild_remove(guild):
        await Configuration.delete_config(guild.id)

    ###########################################

    # Run with Discord oauth token
    client.run(os.getenv("DISCORD_TOKEN"))

# Enable reading .env variables
load_dotenv()

# Configure Discord logging
log_level = (os.getenv("LOG_LEVEL"))
log_mode = (os.getenv("LOG_MODE"))
logger = getLogger('discord')
logger.setLevel(log_level)
handler = FileHandler(filename='DiscordBot.log', encoding='utf-8', mode=log_mode)
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Run main
if __name__ == '__main__':
    main()
