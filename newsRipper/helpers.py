
import json, pandas as pd, unidecode
from bs4 import BeautifulSoup
import requests

def getDocText(url):
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]
    text = soup.find_all(text=True)
    output = ''
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

"""
The Below functions contains error handling, unidecode, digits extraction, dataframe cleaning
"""

errors = {'None': None, 'list': [], 'dict': {}}


def catch(default, func, handle=lambda e: e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        return errors[default]


def unicode(text: str) -> bool:
    return unidecode.unidecode(text).strip()

def news_article(text):
    return unicode(' '.join(text.replace('’', '').split()))


def digits(text: str) -> bool:
    return int(''.join(i for i in text if i.isdigit()))


def dataframe_data(df):
    return df.dropna(how='all').reset_index(drop=True)


def author(soup):
    i = 0
    while True:
        meta = json.loads(soup.select('script[type="application/ld+json"]')[i].text)
        df = catch('None', lambda: pd.DataFrame(meta))
        meta_check = any(word in 'author' for word in list(meta.keys()))
        authors = catch('None', lambda: meta.get('author') if meta_check == True else df['author'][0] if df != None else meta.get('author')['name'] if meta_check == True else meta[0].get('author')['name'] if type(meta) == list else 'N/A')
        if '' != authors or i == 3:
            break
        i += 1
    return author


def date(soup):
    i = 0
    while True:
        meta = json.loads(soup.select('script[type="application/ld+json"]')[i].text)
        df = catch('None', lambda: pd.DataFrame(meta))
        meta_check = any(word in 'datePublished' for word in list(meta.keys()))
        date = catch('None', lambda: meta.get('datePublished') if meta_check == True else df['datePublished'][0] if df != None else meta[0].get('datePublished') if type(meta) == list else 'N/A')
        if '' != date or i == 3:
            break
        i += 1
    return date


def category(soup):
    i = 0
    while True:
        meta = json.loads(soup.select('script[type="application/ld+json"]')[i].text)
        df = catch('None', lambda: pd.DataFrame(meta))
        meta_check = any(word in '@type' for word in list(meta.keys()))
        category = catch('None', meta.get('@type') if meta_check == True else df['@type'][0] if len(df) != 0 else 'N/A')
        if '' != category or i == 3:
            break
        i += 1


def publisher(soup):
    i = 0
    while True:
        meta = json.loads(soup.select('script[type="application/ld+json"]')[i].text)
        df = catch('None', lambda: pd.DataFrame(meta))
        meta_check = any(word in 'publisher' for word in list(meta.keys()))
        publisher = catch('None', lambda: meta.get('publisher') if meta_check == True else df['publisher'][0] if df != None else meta.get('publisher')['name'] if meta_check == True else meta[0].get('publisher')['name'] if type(meta) == list else 'N/A')
        if '' != publisher or i == 3:
            break
        i += 1

    return publisher