from asyncio.log import logger
from tokenize import Double
from discord.ext import commands, tasks
from discord.ext.commands import Cog
import logging
import requests
import os
from ..embed.cog import CustomEmbed
import serverconfig

class Buys(commands.Cog):
    """Monitors and posts KTO buy transactions"""

    #Configure cog logging
    global logger
    logger = logging.getLogger("discord.bot.buys")
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("buys cog initialised")

    #Set the etherscan API call variables
    global Address
    Address = "0x20893b642b56fa81131a8fb1d6489e82de5a7449"
    global TxCount
    TxCount = "20"
    global APIKey
    APIKey = os.getenv("ETHERSCAN_API")
    global APICall
    APICall = f"https://api.etherscan.io/api?module=account&action=tokentx&address={Address}&page=1&offset={TxCount}&sort=desc&apikey={APIKey}"
    global ETHMin
    ETHMin = float(os.getenv("MIN_ETH"))

    #Variable for tracking block number
    global BlockNo
    BlockNo = 0

    @Cog.listener()
    async def on_ready(self):
        self.checkbuys.start()

    @tasks.loop(seconds=10)
    async def checkbuys(ctx):
        global APICall
        global BlockNo
        global ETHMin
        #If block number has been set
        if BlockNo != 0:
            APICall = f"https://api.etherscan.io/api?module=account&action=tokentx&address={Address}&page=1&offset={TxCount}&startblock={BlockNo}&sort=desc&apikey={APIKey}"
            response = requests.get(APICall)
            if response.ok:
                content = response.json()
                #Check if there are any new transactions to process
                if content['message'] != "No transactions found":
                    processed = []
                    #Evaluate each transaction to see if it is a buy and is yet to be processed - if not a buy, add to processed
                    for txn in content['result']:
                        CurrentTxn = txn['hash']
                        if CurrentTxn not in processed:
                            logger.info(f"Processing transaction with hash {CurrentTxn}")
                            #Currency tracking variables
                            KTOReceived = 0
                            KTOReflected = 0
                            KTOTempRec = 0
                            KTOTempRef = 0
                            ETHSpent = 0
                            ETHTemp = 0
                            #Loop through all new transactions to find those matching the current transaction and calcualte total KTO and ETH (multiple transactions due to multicall)
                            for transfer in content['result']:
                                if transfer['hash'] == CurrentTxn:
                                    if transfer['tokenSymbol'] == "KTO":
                                        #This is KTO received
                                        if transfer['from'] == "0x20893b642b56fa81131a8fb1d6489e82de5a7449" and transfer['to'] != "0x616ef40d55c0d2c506f4d6873bda8090b79bf8fc":
                                            KTOTempRec += float(transfer['value']) / 1000000000
                                        #This is KTO reflected
                                        elif transfer['from'] == "0x20893b642b56fa81131a8fb1d6489e82de5a7449" and transfer['to'] == "0x616ef40d55c0d2c506f4d6873bda8090b79bf8fc":
                                            KTOTempRef += float(transfer['value']) / 1000000000
                                        #This is ETH spent
                                    elif transfer['tokenSymbol'] == "WETH" or transfer['tokenSymbol'] == "ETH":
                                        if transfer['to'] == "0x20893b642b56fa81131a8fb1d6489e82de5a7449":
                                            ETHTemp += float(float(transfer['value']) / 1000000000000000000)
                                    else:
                                        logger.warning(f"A DIFFERENT TOKEN SYMBOL WAS FOUND! - Symbol is {transfer['tokenSymbol']}")
                                    #Round and format the values accordingly
                                    KTOReceived = "{:,}".format(round(KTOTempRec))
                                    KTOReflected = "{:,}".format(round(KTOTempRef))
                                    ETHSpent = round(ETHTemp, 4)
                            logger.info(f"Final values - Received: {KTOReceived} - Reflected: {KTOReflected} - ETH: {ETHSpent}")
                            if ((KTOReceived != 0 and KTOReceived != "0") and (ETHSpent != 0 and ETHSpent != "0")):
                                if ETHSpent >= ETHMin:
                                    if KTOReflected == 0 or KTOReflected == "0":
                                        logger.warning("KTO Reflected is 0 - Assuming tax is off and proceeding to create embed")
                                    #Make and send the embed to each server's designated channel
                                    fields = []
                                    fields.append({"name": ":money_with_wings: ETH Spent :money_with_wings: ", "value": f"```{ETHSpent}```", "inline": False})
                                    fields.append({"name": ":moneybag: KTO Received :moneybag:", "value": f"```{KTOReceived}```", "inline": False})
                                    fields.append({"name": ":coin: KTO Reflected :coin:", "value": f"```{KTOReflected}```", "inline": False})
                                    fields.append({"name": "Transaction", "value": f"[View on etherscan](https://etherscan.io/tx/{CurrentTxn})", "inline": False})
                                    logger.info(f"Sending buy with hash {CurrentTxn} to all servers!")
                                    for server_id in serverconfig.configuration:
                                        if serverconfig.configuration[server_id] != None:
                                            if serverconfig.configuration[server_id]["embed_channel_id"] != None:
                                                embed = await CustomEmbed.newembed(ctx, title="NEW KTO BUY!", fields=fields, server_id=server_id)
                                                channel = ctx.bot.get_channel(serverconfig.configuration[server_id]["embed_channel_id"])
                                                await channel.send(embed=embed)
                                else:
                                    logger.info(f"Not creating embed due to the ETH spent value being below the minimum of {ETHMin}")
                            else:
                                logger.info("Not creating embed due to a \'zero value\' being found")
                            processed.append(CurrentTxn)
                        else:
                            logger.info(f"Ignoring transaction {CurrentTxn} as it has already been processed")
                    #Set the new block number
                    BlockNo = float(content['result'][0]['blockNumber'])+1
                    logger.debug(f"Block number set to {BlockNo}")
                else:
                    logger.info(f"No new transactions to process at block {BlockNo}")
        else:
            response = requests.get(APICall)
            if response.ok:
                content = response.json()
            BlockNo = float(content['result'][0]['blockNumber'])+1
            logger.debug(f"Block number set to {BlockNo}")

def setup(bot: commands.Bot):
    bot.add_cog(Buys(bot))
