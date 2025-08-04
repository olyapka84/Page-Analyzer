from bs4 import BeautifulSoup


def parse_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.title.string if soup.title else ''
    h1 = soup.h1.get_text(strip=True) if soup.h1 else ''
    description = ''
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        description = meta['content']
    return h1, title, description
