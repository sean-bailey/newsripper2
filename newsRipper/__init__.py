import subprocess
from bs4 import BeautifulSoup
from newspaper import Article
from newsplease import NewsPlease
from requests import get
from urllib.parse import unquote
from newsRipper.helpers import *
from search_engines import multiple_search_engines
import warnings
#import time
warnings.filterwarnings('ignore')
import os
os.environ['WDM_LOG_LEVEL'] = '0'

#we want to have essentially a wrapper around search-engines-scraper which makes it more intuitive
#for someone who is trying to scrape the news about a particular topic to get where they are trying to go.
#therefore, I think it would be wise to provide a way to list all the available
#search engines (for now I'll use the default), tips on Dorking

class searchnews:
    #we'll need to default to the multiple engine scraper and use all available engines
    def __init__(self,query=None,engines=['all'],pages=10):
        torprocess=None
        self.pages=pages
        self.enginelist=['aol','ask','bing','dogpile','duckduckgo','google','mojeek','startpage','yahoo']#'torch','yahoo']
        #will simply get the results of the query from the list of engines.
        #if the query is empty, it will return information on what engines are available
        #and some google dorking cheatsheets
        self.query = query
        self.engines=engines
        if self.engines==['all']:
            self.engines=self.enginelist
        #I'm having difficulty getting torch and tor to work well...
        #if 'torch' in self.engines:
        #    torprocess=subprocess.Popen(['torpy_socks'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #    while True:
        #        print("standby, starting tor proxy...")
        #        if torprocess.stderr is not None:
        #            line=torprocess.stderr.readline().decode("utf-8")
        #            print(type(line))
        #            if "Start socks proxy at 127.0.0.1:1050" in line:
        #                print(line)
        #                break
        #        else:
        #            print("Waiting for torprocess to be not None")
        #            time.sleep(1)
        #    #stdout, stderr = torprocess.communicate()

        if isinstance(self.engines,list):
            for enginename in self.engines:
                if not enginename in self.enginelist:
                    if torprocess is not None:
                        torprocess.kill()
                    raise ValueError("The available engines are "+str(self.enginelist))
        if self.query is not None:
            multiengines=multiple_search_engines.MultipleSearchEngines(self.engines)
            self.results=multiengines.search(self.query,pages=self.pages)
        else:
            if torprocess is not None:
                torprocess.kill()
            raise ValueError("You will need to specify a search query (query='myquery'). Note that you can use Dorking to improve results! See the dorking cheatsheet here: https://gist.github.com/sundowndev/283efaddbcf896ab405488330d1bbc06")
        if torprocess is not None:
            torprocess.kill()

class rawnews:

    def __init__(self,url):
        self.results=getDocText(url)


class parsenews:

    def __init__(self, uri: str) -> bool:

        self.uri = uri

        """
        :return: Initializing the values with 'None', In case if the below values not able to extracted from the target uri
        """

        # NewsPlease Scraper
        newsplease = catch(
            'None', lambda: NewsPlease.from_url(self.uri, timeout=6))

        # Newspaper3K Scraper
        article = catch('None', lambda: Article(self.uri, timeout=6))
        catch('None', lambda: article.download())
        catch('None', lambda: article.parse())
        catch('None', lambda: article.nlp())

        soup = catch('None', lambda: BeautifulSoup(get(self.uri).text, 'lxml',timeout=6))

        if all([newsplease, article, soup]) == None:
            raise ValueError(
                "Sorry, the page you are looking for doesn't exist'")

        """
        :returns: The News Article
        """
        self.article = catch('None', lambda: news_article(article.text) if article.text !=
                             None else news_article(newsplease.maintext) if newsplease.maintext != None else 'None')

        """
        :returns: The News Authors
        """
        self.authors = catch('list', lambda: newsplease.authors if len(newsplease.authors) != 0 else article.authors if len(
            article.authors) != 0 else unicode([author(soup)]) if author(soup) != None else ['None'])

        """
        :returns: The News Published, Modify, Download Date
        """
        self.date_publish = catch('None', lambda: str(newsplease.date_publish) if str(newsplease.date_publish) != 'None' else article.meta_data[
                                  'article']['published_time'] if article.meta_data['article']['published_time'] != None else date(soup) if date(soup) != None else 'None')

        self.date_modify = catch('None', lambda: str(newsplease.date_modify))

        self.date_download = catch(
            'None', lambda: str(newsplease.date_download))

        """
        :returns: The News Image URL
        """
        self.image_url = catch('None', lambda: newsplease.image_url)

        """
        :returns: The News filename
        """
        self.filename = catch('None', lambda: unquote(newsplease.filename))

        """
        :returns: The News title page
        """
        self.title_page = catch('None', lambda: newsplease.title_page)

        """
        :returns: The News title rss
        """
        self.title_rss = catch('None', lambda: newsplease.title_rss)

        """
        :returns: The News Language
        """
        self.image_url = catch('None', lambda: newsplease.language)

        """
        :returns: The News Publisher
        """
        self.publication = catch('None', lambda: article.meta_data['og']['site_name'] if article.meta_data['og']['site_name'] != None else publisher(
            soup) if publisher(soup) != None else self.uri.split('/')[2] if self.uri.split('/')[2] != None else 'None')

        """
        :returns: The News Category
        """
        meta_check = any(word in 'section' or 'category' for word in list(
            article.meta_data.keys()))
        self.category = catch('None', lambda: article.meta_data['category'] if meta_check == True and article.meta_data['category'] != {} else article.meta_data['section'] if meta_check ==
                              True and article.meta_data['section'] != {} else article.meta_data['article']['section'] if meta_check == True and article.meta_data['article']['section'] != {} else category(soup) if category(soup) != None else 'None')

        """
        :returns: headlines
        """
        self.headline = catch('None', lambda: unicode(article.title) if article.title != None else unicode(
            newsplease.title) if newsplease.title != None else 'None')

        """
        :returns: keywords
        """
        self.keywords = catch('list', lambda: article.keywords)

        """
        :returns: summary
        """
        self.summary = catch('None', lambda: news_article(article.summary))

        """
        :returns: source domain
        """
        self.source_domain = catch('None', lambda: newsplease.source_domain)

        """
        :returns: description
        """
        self.description = catch('None', lambda: news_article(article.meta_description) if article.meta_description != '' else news_article(
            article.meta_data['description']) if article.meta_data['description'] != {} else news_article(newsplease.description) if newsplease.description != None else None)

        """
        :returns: serializable_dict
        """
        self.get_dict = catch('dict', lambda: {'headline': self.headline,
                                               'author': self.authors,
                                               'date_publish': self.date_publish,
                                               'date_modify': self.date_modify,
                                               'date_download': self.date_download,
                                               'image_url': self.image_url,
                                               'filename': self.filename,
                                               'description': self.description,
                                               'publication': self.publication,
                                               'category': self.category,
                                               'source_domain': self.source_domain,
                                               'article': self.article,
                                               'summary': self.summary,
                                               'keyword': self.keywords,
                                               'title_page': self.title_page,
                                               'title_rss': self.title_rss,
                                               'url': self.uri})