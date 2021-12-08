import aiohttp
import decimal

async def getPrice():
        token = "kounotori"
        api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd"
        async with aiohttp.ClientSession() as cs:
                async with cs.get(api_url) as r:
                    if r.status == 200:
                        res = await r.json()
                        raw_price = res['kounotori']['usd']
                        price = decimal.Decimal(raw_price)
                        price = "{:.12f}".format(price)
                        old_price = price
                        return price