"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

# Always prefer setuptools over distutils
import setuptools

keywords = ['newsRipper2','newsripper', "without-api", "google_scraper", 'news_scraper', 'bs4',
'news-extractor', 'crawler', 'extractor', 'news', 'elasticsearch', 'json', 'python', 'nlp', 'data-gathering',
'news-archive', 'news-articles', 'commoncrawl', 'extract-articles', 'extract-information', 'news-scraper', 'spacy']

setuptools.setup(
    name="newsripper2",
    version="0.2",
    author="Sean Bailey",
    author_email="seanbailey518@gmail.com",
    description="newsripper provides a simple python library which scrapes relevant keyword information from news sites using search engines",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sean-bailey/newsripper2",
    keywords = keywords,
    install_requires=['beautifulsoup4', 'pandas', 'news-please', 'newspaper3k', 'unidecode','cchardet'],
    packages = setuptools.find_packages(),
    classifiers=['Development Status :: 4 - Beta',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Developers',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: MIT License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Topic :: Communications :: Email',
              'Topic :: Office/Business',
              'Topic :: Software Development :: Bug Tracking',
              ],
)
