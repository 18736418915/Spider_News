from bs4 import BeautifulSoup
from loguru import logger
from DrissionPage import ChromiumOptions
import requests
import re
from DrissionPage import WebPage

# 创建 WebPage 对象

co = ChromiumOptions().headless()

page = WebPage(chromium_options=co)


def get_news_content(title):
    """主函数：通过标题获取新闻内容"""
    try:
        url = search_news_bing(title)
        # 访问目标网页
        if url:
            page.get(url)

            title = page.ele('tag:h1').text
            # 提取作者信息
            author_info = page.ele('.media-info')
            if author_info:
                author = author_info.ele('.media-name').text
                publish_info = author_info.ele('.media-meta').text
            else:
                author = "Unknown"
                publish_info = "No publish info"
            # 提取文章内容
            content = []
            for p in page.eles('.qnt-p'):
                content.append(p.text.strip())
            # 返回提取的信息
            return {
                "title": title,
                "author": author,
                "publish_info": publish_info,
                "content": content
            }
    except Exception as e:
        logger.error(f"Error in get_news_content: {str(e)}")
    return None


def search_news_bing(query):
    """使用Bing搜索获取新闻URL"""
    try:
        search_url = f"https://www.bing.com/search?q={query} site:news.qq.com"
        response = requests.get(search_url, headers=get_headers())
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找第一个搜索结果的链接
        result = soup.find('li', class_='b_algo')
        if result:
            link = result.find('a')
            print("测试", link)
            if link:
                return link['href']
    except Exception as e:
        logger.error(f"Error in search_news_bing: {str(e)}")
    return None


def extract_content(html):
    """从HTML中提取新闻内容"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        content_selectors = [
            'article .content',
            '#main-content',
            '.story-body',
            '.article-body',
            '.entry-content',
            '#article-content',
        ]

        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                return clean_content(content.get_text(strip=True))

        # 如果上述选择器都没有找到内容，尝试提取所有段落
        paragraphs = soup.find_all('p')
        if paragraphs:
            return clean_content(' '.join([p.get_text(strip=True) for p in paragraphs]))

        logger.warning("Could not extract content with predefined selectors")
        return None
    except Exception as e:
        logger.error(f"Error in extract_content: {str(e)}")
    return None


def clean_content(text):
    """清理和格式化提取的内容"""
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    # 这里可以添加更多的清理规则
    return text


def get_headers():
    """获取请求头"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


# 使用示例
if __name__ == "__main__":
    datas = requests.get("https://api.lolimi.cn/API/jhrb/?hot=%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1").json().get('data')
    for data in datas:
        news_title = data.get('title')
        article_data = get_news_content(news_title)
        if article_data:
            print(f"标题: {article_data['title']}")
            print(f"作者: {article_data['author']}")
            print(f"发布信息: {article_data['publish_info']}")
            print("\n文章内容:")
            for paragraph in article_data['content']:
                print(paragraph)
                print()  # 添加空行以分隔段落
        else:
            print(f"Failed to retrieve content for '{news_title}'")
