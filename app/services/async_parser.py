from lxml import html


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape(session, url):
    html_content = await fetch(session, url)
    return await parsing(html_content)


async def parsing(html_content):
    tree = html.fromstring(html_content)
    paragraphs = tree.cssselect('.Paragraph_paragraph__nYCys')
    texts = [paragraph.text_content().strip() for paragraph in paragraphs]
    return ' '.join(texts)
