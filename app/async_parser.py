from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape(session, url):
    html_content = await fetch(session, url)
    return await parsing(html_content)


async def parsing(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all(class_="Paragraph_paragraph__nYCys")
    texts = [article.text for article in articles]
    return ' '.join(texts)
