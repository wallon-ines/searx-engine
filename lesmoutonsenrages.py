"""
 alterjt (Web)

 @website     http://lesmoutonsenrages.fr/
 @provide-api ?
 @using-api   no
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from cgi import escape
from urllib import urlencode
from lxml import html
from searx.search import logger
import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

logger = logger.getChild('lesmoutonsenrages')

# engine dependent config
categories = ['information', 'general']
paging = True


# search-url http://lesmoutonsenrages.fr/page/2/?s=var
base_url = 'https://lesmoutonsenrages.fr/'
search_url = 'page/{page}/?s={query}'

results_xpath = '//article[contains(@class, "post")]'
url_xpath = './/h2[contains(@class, "entry-title")]/a/@href'
title_xpath = './/h2[contains(@class, "entry-title")]/a//text()'
content_xpath = './/div[contains(@class, "entry")]]/p//text()' #TODO

def request(query, params):
    host = base_url
    params['url'] = host + search_url.format(page=params['pageno'] -1,
                                             query=query)
    return params


# get response from search-request
def response(resp):
    dom = html.fromstring(resp.text)
    results = []
    for result in dom.xpath(results_xpath):
        try:
            res = {'url': result.xpath(url_xpath)[0],
                   'title': escape(''.join(result.xpath(title_xpath)))}
                   #'content': escape(''.join(result.xpath(remove_tags(content_xpath))))} #TODO

        except:
            logger.exception('Erreur: lesmoutonsenrages')
            continue

        results.append(res)

    return results
