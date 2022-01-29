#Import required components
import asyncio
import logging
import discord
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord.commands import Option
import time

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
Description = 'Official KTO Tax Bot'
Intents = discord.Intents.default()
Delay = 8 #Setting this any higher can cause issues with Discord heartbeat
OldAmount = None
UseDollar = False

#Set activity variables
ActivityType = discord.ActivityType.watching
ActivityName = 'KTO Tax Rate'
Activity = discord.Activity(type=ActivityType, name=ActivityName)

#Set file path variables
DataSource = '//DOMCON_1/KTO_Data/KTO_Tax.txt'
OauthSource = './Oauth.txt'

#Read the oauth token from a file
with open(OauthSource) as f:
        Token = f.readline().rstrip()
        f.close()
 
#Instantiate the bot
DiscBot = Bot(command_prefix=Prefix, description=Description, intents=Intents)

#Define the "/GetTimestamp" command
@DiscBot.slash_command(
    name="timestamp",
    description="Returns a local timestamp, relative to the user viewing it.",
    guild_ids=[
        893600091686981722
    ]
)
@has_permissions(administrator=True)
async def Timestamp(
    ctx,
    inputtime: Option(str, 'Format: dd.mm.yyyy.HH.MM.SS', required=True, default=None),
    outformat: Option(str, 'Format to output (default: Short Date/Time)', required=True, default=None,
                    choices=(
                        'Short Time (HH:MM)',
                        'Long Time (HH:MM:SS)',
                        'Short Date (dd/mm/yyyy)',
                        'Long Date (dd month yyyy)',
                        'Short Date/Time (dd month yyyy HH:MM)',
                        'Long Date/Time (day, dd month yyyy HH:MM)',
                        'Relative Time (X time ago/from now)'
                    )
                )
):
    logging.info("Starting Timestamp function...")
    if inputtime == None:
        await ctx.respond("No inputtime provided! Please try again.")
    else:
        date_time=inputtime
        pattern='%d.%m.%Y.%H.%M.%S'
        match outformat:
            case 'Short Time (HH:MM)':
                format='t'
            case 'Long Time (HH:MM:SS)':
                format='T'
            case 'Short Date (dd/mm/yyyy)':
                format='d'
            case 'Long Date (dd month yyyy)':
                format='D'
            case 'Short Date/Time (dd month yyyy HH:MM)':
                format='f'
            case 'Long Date/Time (day, dd month yyyy HH:MM)':
                format='F'
            case 'Relative Time (X time ago/from now)':
                format='R'
        try:
            EpochTime=int(time.mktime(time.strptime(date_time, pattern)))
            await ctx.respond(f"The time code for {date_time} is below.\n\\<t:" + str(EpochTime) + ":" + format + ">")
            logging.info("Timestamp executed successfully!")
        except Exception as e:
            logging.warning(e)
            await ctx.respond("Incorrect datetime format! Please try again.")
@Timestamp.error
async def GetTimestamp_Error(ctx, error):
    if isinstance(error, MissingPermissions):
        BotError=discord.Embed(
            title="Permission Denied!",
            description="You do not have sufficient permissions to run that command!",
            color=0xff7573
        )
    else:
        BotError=discord.Embed(
            title="Application Error!",
            description="The application encountered an error and could not complete the command.",
            color=0xff7573
        )
        logging.error(error)
    await ctx.respond(embed=BotError)

#Define the "/tax" command
@DiscBot.slash_command(
    name="tax",
    description="Returns a breakdown of current KTO tax rates."
)
async def tax(ctx):
    #Load the data
    with open('//DOMCON_1/KTO_Data/Tax_Details/BuyMTax.txt') as f:
        BuyMTax = f.readline().rstrip()
        f.close()
    with open('//DOMCON_1/KTO_Data/Tax_Details/BuyReflect.txt') as f:
        BuyReflect = f.readline().rstrip()
        f.close()
    with open('//DOMCON_1/KTO_Data/Tax_Details/SellMTax.txt') as f:
        SellMTax = f.readline().rstrip()
        f.close()
    with open('//DOMCON_1/KTO_Data/Tax_Details/SellReflect.txt') as f:
        SellReflect = f.readline().rstrip()
        f.close()
    with open('//DOMCON_1/KTO_Data/Tax_Details/TferMtax.txt') as f:
        TferMtax = f.readline().rstrip()
        f.close()
    with open('//DOMCON_1/KTO_Data/Tax_Details/TferReflect.txt') as f:
        TferReflect = f.readline().rstrip()
        f.close()
    #Build the embed
    TaxDetail = discord.Embed(
        title="KTO Tax Breakdown",
        description="",
        color=0xff7573
    )
    TaxDetail.add_field(
        name="Buy Tax:",
        value="Reflections: " + BuyReflect + "\nMarketing: " + BuyMTax,
        inline=False
    )
    TaxDetail.add_field(
        name="Sell Tax:",
        value="Reflections: " + SellReflect + "\nMarketing: " + SellMTax,
        inline=False
    )
    TaxDetail.add_field(
        name="Transfer Tax:",
        value="Reflections: " + TferReflect + "\nMarketing: " + TferMtax,
        inline=False
    )
    TaxDetail.set_footer(
        text="Requested by: {}".format(ctx.author.display_name)
    )
    #Send the embed
    await ctx.respond(embed=TaxDetail)

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
        await (DiscGuild.get_member(DiscBot.user.id)).edit(nick=Amount)
        logging.info("Updated nickname for server %s", DiscGuild)
    logging.info("Updated ALL nicknames")

#Function to update the nickname on one server (to ensure new servers perform a quick initial update)
async def updateOneNickname(Amount,DiscGuild):
    logging.info("Updating nickname on %s", DiscGuild)
    await (DiscGuild.get_member(DiscBot.user.id)).edit(nick=Amount)
    logging.info("Updated nickname to %s", Amount)

#Function to check that the nickname in all servers is set appropriately
async def checkNickname(Amount):
    logging.debug("Checking nicknames on ALL servers")
    async for guild in DiscBot.fetch_guilds(limit=100):
        DiscGuild = DiscBot.get_guild(guild.id)
        CurrentNick = (DiscGuild.get_member(DiscBot.user.id)).nick
        if CurrentNick != Amount:
            logging.info("Nickname in server %s is not correct", DiscGuild)
            await updateOneNickname(Amount,DiscGuild)

#Main function that controls the frequency of retrieving data and updating nicknames
async def loop():
    while True:
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
    DiscBot.loop.create_task(loop())

DiscBot.run(Token)
