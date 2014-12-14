import requests
from bs4 import BeautifulSoup, NavigableString
import unicodedata

def retrieve_text(url):
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception()

    soup = BeautifulSoup(req.text)


    #remove script tag
    script = soup.find_all('script')
    style = soup.find_all('style')
    nav = soup.find_all('nav')
    link = soup.find_all('a')
    form = soup.find_all('form')

    [sc.extract() for sc in script]
    [st.extract() for st in style]
    [nv.extract() for nv in nav]
    [l.extract() for l in link]
    [f.extract() for f in form]
    if soup.head:
        soup.head.extract()
    if soup.header:
        soup.header.extract()

    # remove all other content
    '''other = []
    for i in soup.find_all(True):
        if (i.name == "html" or i.name == "body"):
            continue
        for j in i.descendants:
            if j.name == "h1":
                break
        else:
            other.append(i)

        break
    [i.extract() for i in other]'''

    text = soup.get_text()
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    return text
