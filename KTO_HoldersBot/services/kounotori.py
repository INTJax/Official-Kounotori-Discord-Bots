import decimal

async def getHolders():
        with open('C:\Delivery\Scripts\KTO_HoldersBot\Holders.txt') as f:
                holders = f.readline().rstrip()
        print('TOKEN HOLDERS: ', holders)
        return holders
