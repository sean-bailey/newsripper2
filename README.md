# newsripper

Newsripper leverages the search engines found here: https://github.com/sean-bailey/Search-Engines-Scraper to then perform deep article sumarization and analyiis by leveraging the search engines available there.

**Prerequisites**
-
1) Python3.7+
   
2) `REQUIREMENTS.txt`

**Installation**
-

```pip install -r REQUIREMENTS.TXT```

```pip install .```

**Usage**
-
To get the results from your requested search:

```
import newsRipper as nr
#to get results from all available search engines:
results=nr.searchnews(query="TSLA site:www.cnn.com & (before:2000-01-01 after:2001-01-01)").results

#to get results from a particular set of search engines:
results=nr.searchnews(query="TSLA site:www.cnn.com & (before:2000-01-01 after:2001-01-01)",engines=['google','yahoo','bing']).results

#this returns the results from search_engines, which includes
# .links, .text, .hosts, titles
```

If you have a list of links you'd like to now parse,

```
import newsRipper as nr

for url in nr.searchnews(query="TSLA site:www.cnn.com & (before:2000-01-01 after:2001-01-01)").results.links():
    if nr.parsenews(url).date_publish is not None:
        news = nr.parsenews(url)
        print(news.date_publish)
        print(news.headline)
        print(news.keywords)
        print(news.summary)

```

If you'd just like to get the raw text from a given url:

```
import newsRipper as nr:

rawtext=nr.rawnews("https://en.wikipedia.org/wiki/Hannah_Glasse").results

```

I have found that search-engines-scraper provides just the text which appears in the search results themselves. 
This library takes this to its logical conclusion, gathering the article information and metadata in its entirety.

**Contributing**
-
If you find a bug, please submit it in the issues tab!
If you'd like to contribute, fork this repository, make your changes, and do a pull request to this repository.