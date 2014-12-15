import requests
from bs4 import BeautifulSoup, NavigableString
import unicodedata
import itertools


def retrieve_text(url):
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception()

    soup = BeautifulSoup(req.text)

    # remove other tag
    script = soup.find_all('script')
    style = soup.find_all('style')
    nav = soup.find_all('nav')
    form = soup.find_all('form')
    all_tag = list(itertools.chain(script, style, nav, form))

    [tag.extract() for tag in all_tag]

    if soup.head:
        soup.head.extract()
    if soup.header:
        soup.header.extract()

    text = soup.get_text()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    return text
