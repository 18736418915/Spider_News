import aiohttp
import asyncio
import json

"""
https://tenapi.cn/v2/baiduhot  百度热点
https://tenapi.cn/v2/douyinhot  抖音热点
https://tenapi.cn/v2/weibohot  微博热点
https://tenapi.cn/v2/zhihuhot  知乎热点
https://tenapi.cn/v2/bilihot  哔哩哔哩热点
https://tenapi.cn/v2/toutiaohot  头条热点
https://tenapi.cn/v2/toutiaohotnew  今日头条热点新闻
"""


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
