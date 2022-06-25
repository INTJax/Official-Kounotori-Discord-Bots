from asyncio.log import logger
from asyncio import sleep
from discord.ext import commands, tasks
from discord.ext.commands import Cog
from discord.commands import slash_command
import logging
import requests
import os
from ..embed.cog import CustomEmbed
from web3 import Web3
import serverconfig

class Tax(commands.Cog):
    """Keeps track of and updates it's nickname to the KTO tax values"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.tax")
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("tax cog initialised")
    
    #Set variable for amount difference tracking
    global OldAmount
    OldAmount = "0"

    #Set the required Web3 variables
    web3URL = os.getenv("WEB3_URL")
    web3 = Web3(Web3.HTTPProvider(web3URL))

    #Get the contract ABI
    address = "0x616ef40D55C0D2c506f4d6873Bda8090b79BF8fC"
    APIKey = os.getenv("ETHERSCAN_API")
    APICall = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={APIKey}"
    response = requests.get(APICall)
    while not response.ok:
        logger.warning("API call to Etherscan did not return OK. Trying again in 3 seconds...")
        sleep(3)
        response = requests.get(APICall)
    if response.ok:
            content = response.json()
            abi = content['result']

    #Set the contract object
    global contract
    contract = web3.eth.contract(address=address, abi=abi)

    #Perform initial set of tax values
    global buyTaxes, sellTaxes, transferTaxes
    buyTaxes = contract.functions._buyTaxes().call()
    sellTaxes = contract.functions._sellTaxes().call()
    transferTaxes = contract.functions._transferTaxes().call()
     
    @Cog.listener()
    async def on_ready(self):
        self.updatevalue.start()

    #Function to retrieve the required KTO data
    async def getKTOData():
        global contract, buyTaxes, sellTaxes, transferTaxes
        buyTaxes = contract.functions._buyTaxes().call()
        sellTaxes = contract.functions._sellTaxes().call()
        transferTaxes = contract.functions._transferTaxes().call()
        return f"{int((buyTaxes[0]+buyTaxes[2])/100)}% | {int((sellTaxes[0]+sellTaxes[2])/100)}% | {int((transferTaxes[0]+transferTaxes[2])/100)}%"

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
                    await Tax.updateOneNickname(ctx, Amount, DiscGuild)
    
    #Main function that controls the frequency of retrieving data and updating nicknames
    @tasks.loop(seconds=10)
    async def updatevalue(ctx):
        logger.info("Checking for new tax...")
        global OldAmount
        Amount = await Tax.getKTOData()
        if Amount != OldAmount:
            logger.info("Amount has changed to %s", Amount)
            await Tax.updateNickname(ctx, Amount)
            OldAmount = Amount
        else:
            logger.info("Amount has not changed")
            await Tax.checkNickname(ctx, Amount)

    @slash_command()
    async def tax(self, ctx):
        fields = []
        fields.append({"name": f"BUY - {int((buyTaxes[0]+buyTaxes[2])/100)}%", "value": f"```Reflections: {int(buyTaxes[0]/100)}%\nMarketing: {int(buyTaxes[2]/100)}%```", "inline": False})
        fields.append({"name": f"SELL - {int((sellTaxes[0]+sellTaxes[2])/100)}%", "value": f"```Reflections: {int(sellTaxes[0]/100)}%\nMarketing: {int(sellTaxes[2]/100)}%```", "inline": False})
        fields.append({"name": f"TRANSFER - {int((transferTaxes[0]+transferTaxes[2])/100)}%", "value": f"```Reflections: {int(transferTaxes[0]/100)}%\nMarketing: {int(transferTaxes[2]/100)}%```", "inline": False})
        footer = f"Requested by: {ctx.author.display_name}"
        embed = await CustomEmbed.newembed(ctx, title="KTO TAX BREAKDOWN", description="", fields=fields, footer=footer)
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Tax(bot))
