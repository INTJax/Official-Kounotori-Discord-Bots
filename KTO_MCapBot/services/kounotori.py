import decimal

async def getKTOMCap():
        with open('//DOMCON_1/KTO_Data/KTO_MCap.txt') as f:
                KTOMCap = f.readline().rstrip()
        return KTOMCap
