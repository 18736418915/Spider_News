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
import aiohttp
import asyncio
import json
from aiohttp import ClientTimeout
from contextlib import suppress
import time


async def fetch_json(session, url):
    try:
        async with session.get(url, timeout=ClientTimeout(total=10)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"code": response.status, "msg": "HTTP error", "data": []}
    except Exception as e:
        return {"code": 0, "msg": str(e), "data": []}


async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=ClientTimeout(total=10)) as response:
            if response.status == 200:
                return await response.text()
            else:
                return f"Error: HTTP {response.status}"
    except Exception as e:
        return f"Error: {str(e)}"


async def process_url(session, semaphore, url):
    async with semaphore:
        return await fetch_html(session, url)


async def main():
    urls = [
        "https://tenapi.cn/v2/baiduhot",
        "https://tenapi.cn/v2/douyinhot",
        "https://tenapi.cn/v2/weibohot",
        "https://tenapi.cn/v2/zhihuhot",
        "https://tenapi.cn/v2/bilihot",
        "https://tenapi.cn/v2/toutiaohot",
        "https://tenapi.cn/v2/toutiaohotnew"
    ]

    async with aiohttp.ClientSession() as session:
        json_tasks = [fetch_json(session, url) for url in urls]
        json_responses = await asyncio.gather(*json_tasks)

        semaphore = asyncio.Semaphore(5)  # Limit concurrent requests
        html_tasks = []
        for response in json_responses:
            if response['code'] == 200:
                for item in response['data']:
                    html_tasks.append(process_url(session, semaphore, item['url']))

        html_responses = await asyncio.gather(*html_tasks)

    for url, html in zip(
            [item['url'] for response in json_responses if response['code'] == 200 for item in response['data']],
            html_responses):
        print(f"HTML content from {url}:")
        print(html[:200])  # Print first 200 characters of HTML
        print("\n")


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        start_time = time.time()
        asyncio.run(main())
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")
