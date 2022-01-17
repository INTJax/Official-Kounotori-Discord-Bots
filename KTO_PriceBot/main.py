#Import required components
import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand
import asyncio
import logging

#Set up logging
LogName = 'DiscBot.log'
LogMode = 'a' # r = read only; w = truncate then write; x = create only; a = append; b = binary mode; t = text mode (default); + = update;
LogFormat = '%(asctime)s %(name)s %(levelname)s %(message)s'
LogDateFormat = '%Y-%m-%d %H:%M:%S'
LogLevel = logging.INFO
logging.basicConfig(
    filename = LogName,
    filemode = LogMode,
    format = LogFormat,
    datefmt = LogDateFormat,
    level = LogLevel
)
logging.info("********** STARTING NEW INSTANCE **********")

#Set start up variables
Prefix = '$'
Description = 'Official KTO Price Bot'
Intents = discord.Intents.default()
Delay = 8 #Setting this any higher can cause issues with Discord heartbeat
OldAmount = None
UseDollar = False

#Set activity variables
ActivityType = discord.ActivityType.watching
ActivityName = 'KTO Price'
Activity = discord.Activity(type=ActivityType, name=ActivityName)

#Set file path variables
DataSource = '//DOMCON_1/KTO_Data/KTO_Price.txt'
OauthSource = './Oauth.txt'

#Read the oauth token from a file
with open(OauthSource) as f:
        Token = f.readline().rstrip()
        f.close()
 
#Instantiate the bot
DiscBot = Bot(command_prefix=Prefix, description=Description, intents=Intents)
Slash = SlashCommand(DiscBot, sync_commands=True)

#Function to retrieve the required KTO data
async def getKTOData():
    logging.debug("Getting KTO data...")
    with open(DataSource) as f:
        KTOData = f.readline().rstrip()
        f.close()
        return KTOData

#Function to update the nickname on all servers
async def updateNickname(Amount):
    logging.info("Updating ALL nicknames to %s", Amount)
    async for guild in DiscBot.fetch_guilds(limit=100):
        DiscGuild = DiscBot.get_guild(guild.id)
        await (DiscGuild.get_member(user_id=DiscBot.user.id)).edit(nick=Amount)
        logging.info("Updated nickname for server %s", DiscGuild)
    logging.info("Updated ALL nicknames")

#Function to update the nickname on one server (to ensure new servers perform a quick initial update)
async def updateOneNickname(Amount,DiscGuild):
    logging.info("Updating nickname on %s", DiscGuild)
    await (DiscGuild.get_member(user_id=DiscBot.user.id)).edit(nick=Amount)
    logging.info("Updated nickname to %s", Amount)

#Function to check that the nickname in all servers is set appropriately
async def checkNickname(Amount):
    logging.debug("Checking nicknames on ALL servers")
    async for guild in DiscBot.fetch_guilds(limit=100):
        DiscGuild = DiscBot.get_guild(guild.id)
        CurrentNick = (DiscGuild.get_member(user_id=DiscBot.user.id)).nick
        if CurrentNick != Amount:
            logging.info("Nickname in server %s is not correct", DiscGuild)
            await updateOneNickname(Amount,DiscGuild)

#Main function that controls the frequency of retrieving data and updating nicknames
async def loop():
    Amount = await getKTOData()
    global UseDollar
    if UseDollar:
        Amount = "$" + Amount
    global OldAmount
    if Amount != OldAmount:
        logging.info("Amount has changed to %s", Amount)
        await updateNickname(Amount)
        OldAmount = Amount
    else:
        logging.debug("Amount has not changed")
        await checkNickname(Amount)
    global Delay
    await asyncio.sleep(Delay)

#Set the bot's activity and initiate the main loop
@DiscBot.event
async def on_ready():
    await DiscBot.wait_until_ready()
    logging.info("Logged in as %s", DiscBot.user)
    logging.info("My user ID is %s", DiscBot.user.id)
    await DiscBot.change_presence(activity = Activity)
    logging.info("Activity set to %s", Activity)
    logging.info("Starting loop")
    while True:
        await loop()

DiscBot.run(Token)
