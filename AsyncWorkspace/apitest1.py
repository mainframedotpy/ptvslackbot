import asyncio
import logging
import pathlib
import datetime as dt
from hashlib import sha1
import hmac
import sys

import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr
    )
logger = logging.getLogger("aiotest1")
logging.getLogger("chardt.charsetprober").disabled = True


async def checkline(session, routeid):
    logger.info(f"fetching route {routeid}")

    req = f'/v3/disruptions/route/{routeid}'
    url1 = await getsigurl(req)

    async with session.get(url1) as response:
        lineinfo = await response.json()

    logger.info(f"finished fetching route {routeid}")
    return lineinfo


async def checkall(session):
    # tiem check
    req = '/v3/routes?route_types=1'
    url1 = await getsigurl(req)

    async with session.get(url1) as response:
        return await response.json()


async def getsigurl(request):
    devid = ''
    key = ''

    # Define constants for request url
    baseurl = 'http://timetableapi.ptv.vic.gov.au'

    request = request + ('&' if ('?' in request) else '?')
    raw = request + 'devid={}'.format(devid)
    hashed = hmac.new(key.encode('utf-8'), raw.encode('utf-8'), sha1)
    sig = hashed.hexdigest()
 
    # Return a workable url
    return baseurl + raw + '&signature={}'.format(sig)


async def main():
    idlist = [str(i) for i in range(1, 18) if i != 10]

    async with ClientSession() as session:
        refresh = []
        for i in idlist:
            refresh.append(checkline(session, i))
    
        result = await asyncio.gather(*refresh)

        # print(result[0])
        for i in result:
            for x in i['disruptions']['metro_train']:
                if x["display_on_board"] == True:
                    print(x["description"])


asyncio.run(main())