import decimal

async def getHolders():
        with open('//DOMCON_1/KTO_Data/KTO_Holders.txt') as f:
                holders = f.readline().rstrip()
        return holders
