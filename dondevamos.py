"""
 dondevamos (Web)

 @website     http://dondevamos.canalblog.com
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

logger = logger.getChild('Dondevamos')

# engine dependent config
categories = ['pedophilie', 'general']
paging = True
language_support = True  # TODO


# search-url http://www.canalblog.com/search/posts/var%20site%3Adondevamos.canalblog.com/page/2
base_url = 'http://www.canalblog.com'
search_url = '/search/posts/{query}%20site%3Adondevamos.canalblog.com/page/{page}'

results_xpath = '//div[@id="content"]/div[@class="block"]/div[@class="holder"]/div[@class="frame"]/div[@class="content"]/div[@class="results"]/ul[contains(@class, "item-list-2")]/li/div[@class="item-info"]'
url_xpath = './/span/a/@href'
title_xpath = './/span/a//text()'
content_xpath = './/div[@class="item_excerpt"]//text()'


def request(query, params):
    host = base_url
    params['url'] = host + search_url.format(page=params['pageno'],
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
            logger.exception('Erreur: Dondevamos')
            continue

        results.append(res)

    return results
