import decimal

async def getKTOTax():
        with open('//DOMCON_1/KTO_Data/KTO_Tax.txt') as f:
                KTOTax = f.readline().rstrip()
        return KTOTax
