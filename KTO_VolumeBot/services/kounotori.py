import decimal

async def getKTOVolume():
        with open('//DOMCON_1/KTO_Data/KTO_Volume.txt') as f:
                KTOVolume = f.readline().rstrip()
        return KTOVolume
