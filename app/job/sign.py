import asyncio
import aiohttp
import json
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# logging.FileHandler('timer.log')
logging.basicConfig(level=logging.DEBUG, 
    format='%(filename)20s%(lineno)04d[%(message)s]', filename='timer.log')

def foo():
    print('foo')


def mgqr_login():
    try:
        cookie = CookieJar()
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler = HTTPCookieProcessor(cookie)
        # 通过handler来构建opener
        opener = build_opener(handler)
        req = Request(url='http://www.mgqr.com/control/checklogin.ashx',
                      data=b'UserName=1392798578%40qq.com&UserPwd=111aaa&remember=1')
        # 此处的open方法同urllib2的urlopen方法，也可以传入request
        response = opener.open(req)
        text = response.read()
        logger.info(text)
        obj = json.loads(text, )
        req1 = Request(
            "http://www.mgqr.com/control/userres.ashx?q={}".format(
                random.random()),
            data=b"")
        response1 = opener.open(req1)
        logger.debug(response1.read().decode("utf8"))
        result = {}
    except Exception as e:
        traceback.print_exc()


async def fetch():
    session: aiohttp.client.ClientSession = None
    data = 'UserName={}&UserPwd={}&remember=1'.format('nxlqhmr', '111aaa')
    async with aiohttp.ClientSession() as session:
        async with session.post('http://www.mgqr.com/control/checklogin.ashx',
                                data=data.encode('latin-1')) as resposne:
            text = await resposne.text()
            jsnRsp = json.loads(text)
            logging.debug(text)

if __name__ == '__main__':
    # loop: asyncio.windows_events._WindowsSelectorEventLoop = asyncio.get_event_loop()
    # loop.run_until_complete(fetch())
    if True:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(fetch, 'interval', minutes=3, id='fetch')
        scheduler.start()
        asyncio.get_event_loop().run_forever()
