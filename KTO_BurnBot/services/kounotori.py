import decimal

async def getBurntKTO():
        with open('//DOMCON_1/KTO_Data/KTO_Burnt.txt') as f:
                BurntKTO = f.readline().rstrip()
        return BurntKTO
