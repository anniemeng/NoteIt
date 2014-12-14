import requests
from bs4 import BeautifulSoup, NavigableString
import unicodedata

def retrieve_text(url):
    '''
    >>> retrieve_text('https://developers.google.com/fonts/docs/developer_api')

    '''
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception()

    soup = BeautifulSoup(req.text)


    #remove script tag
    script = soup.find_all('script')
    nav = soup.find_all('nav')
    [sc.extract() for sc in script or nav]
    soup.head.extract()

    # remove all other content
    '''other = []
    for i in soup.find_all(True):
        print("THIS IS I ")
        print(i.name)
        if (i.name == "html" or i.name == "body"):
            continue
        for j in i.descendants:
            if j.name == "h1":
                break
        else:
            other.append(i)
            continue
        break
    [i.extract() for i in other]'''

    text = soup.get_text()
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    #text = text.split("\n")
    return text



def main():
    import doctest
    options = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print "Running doctests..."
    doctest.testmod(optionflags=options)


if __name__ == "__main__":
    main()
