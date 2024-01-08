import re

from lxml import html


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape(session, url, html_class):
    html_content = await fetch(session, url)
    return await parsing(html_content, html_class)


async def parsing(html_content, html_classes):
    tree = html.fromstring(html_content)
    result = {}
    for html_class in html_classes:
        paragraphs = tree.cssselect(html_class)
        result[html_class] = [re.sub(r'\s+', ' ', paragraph.text_content().strip()) for paragraph in paragraphs]
    return result
