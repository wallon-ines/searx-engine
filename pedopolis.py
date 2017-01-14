"""
pedopolis (Web)

 @website     https://pedopolis.com/
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

logger = logger.getChild('pedopolis')

# engine dependent config
categories = ['pedophilie', 'general']
paging = True


# search-url https://globalepresse.net/?s=var
base_url = 'https://pedopolis.com/'
search_url = 'page/{page}/?s={query}'

results_xpath = '//article'
url_xpath = './/header[@class="entry-header"]/h1[@class="entry-title"]/a/@href'
title_xpath = './/header[@class="entry-header"]/h1[@class="entry-title"]/a//text()'
content_xpath = './/div[@class="entry-summary"]/p//text()'
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
                   'title': escape(''.join(result.xpath(title_xpath))),
                   'content': escape(''.join(result.xpath(content_xpath)))}

        except:
            logger.exception('Erreur: globalepresse')
            continue

        results.append(res)

    return results
