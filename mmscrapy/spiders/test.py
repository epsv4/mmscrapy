import requests
import bs4
import itertools
import typing
import scrapy


if 0:
    resp: requests.Response = requests.get(
        'http://cl.z829.pw/thread0806.php?fid=8&search=&page=4')
    print(resp.content.decode('gbk'))
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(resp.content)
    ax = soup.select('#ajaxtable > tbody > tr  > td.tal > h3 > a')
    nextPage: str = list(filter(
        lambda x: x.contents[0] == "下一頁", soup.select('div.pages a')))[0].attrs['href']
    print(ax)
    print(nextPage)
    resp1 : requests.Response = requests.get('http://cl.z829.pw/htm_data/8/1802/2984988.html')
    soup1 : bs4.BeautifulSoup = bs.BeautifulSoup(resp1.content)
    soup1.select('div.tpc_content > input[type="image"]')