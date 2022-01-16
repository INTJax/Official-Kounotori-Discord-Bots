import decimal

async def getKTOSupply():
        with open('//DOMCON_1/KTO_Data/KTO_Supply.txt') as f:
                KTOSupply = f.readline().rstrip()
        return KTOSupply
