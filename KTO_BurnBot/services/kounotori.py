import decimal

async def getBurntKTO():
        with open('C:\Delivery\Scripts\KTO_BurnBot\BurntKTO.txt') as f:
                BurntKTO = f.readline().rstrip()
        print('BURNT KTO: ', BurntKTO)
        return BurntKTO
