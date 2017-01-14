"""
 alterjt (Web)

 @website     http://www.alterjt.tv/
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

logger = logger.getChild('alterjt')

# engine dependent config
categories = ['information', 'general']
paging = True


# search-url http://www.alterjt.tv/page/2/?s=var
base_url = 'http://www.alterjt.tv/'
search_url = 'page/{page}/?s={query}'

results_xpath = '//div[contains(@class, "post")]'
url_xpath = './/div[contains(@class, "entry")]/h2[@class="post-title"]/a/@href'
title_xpath = './/div[contains(@class, "entry")]/h2[@class="post-title"]/a//text()'
content_xpath = './/p//text()'
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
            logger.exception('Erreur: alterjt')
            continue

        results.append(res)

    return results
