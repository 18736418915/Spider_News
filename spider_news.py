import aiohttp
import asyncio
import json
from aiohttp import ClientTimeout,ClientError
from contextlib import suppress
import time
import re


async def fetch_json(session, url):
    try:
        async with session.get(url, timeout=ClientTimeout(total=30)) as response:
            if response.status == 200:
                content = await response.text()
                # 尝试从HTML中提取JSON
                json_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                else:
                    # 如果没有找到JSON，尝试直接解析整个内容
                    return json.loads(content)
            else:
                print(f"HTTP error for {url}: {response.status}")
                return {"code": response.status, "msg": "HTTP error", "data": []}
    except ClientError as e:
        print(f"Client error for {url}: {str(e)}")
        return {"code": 0, "msg": str(e), "data": []}
    except asyncio.TimeoutError:
        print(f"Timeout error for {url}")
        return {"code": 0, "msg": "Timeout", "data": []}
    except Exception as e:
        print(f"Unexpected error for {url}: {str(e)}")
        return {"code": 0, "msg": str(e), "data": []}


async def main():
    urls = [
        "https://tenapi.cn/v2/baiduhot",
        "https://tenapi.cn/v2/douyinhot",
        "https://tenapi.cn/v2/weibohot",
        "https://tenapi.cn/v2/zhihuhot",
        "https://tenapi.cn/v2/bilihot",
        "https://tenapi.cn/v2/toutiaohot"
    ]

    async with aiohttp.ClientSession() as session:
        json_tasks = [fetch_json(session, url) for url in urls]
        json_responses = await asyncio.gather(*json_tasks)
        
        all_items = []
        for url, response in zip(urls, json_responses):
            print(f"Response from {url}:")
            print(response)
            if response['code'] == 200:
                for item in response['data']:
                    all_items.append({
                        'source': url.split('/')[-1],
                        'name': item['name'],
                        'url': item['url']
                    })
            else:
                print(f"Failed to fetch data from {url}")

    # Print or process the collected items
    for item in all_items:
        print(f"Name: {item['name']}")
        print(f"URL: {item['url']}")
        print("---")

    print(f"Total items collected: {len(all_items)}")

if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        start_time = time.time()
        asyncio.run(main())
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")
