"""
 atlantico (Web)

 @website     http://wanted-pedo.com
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

logger = logger.getChild('wanted-pedo')

# engine dependent config
categories = ['pedophilie', 'general']
paging = True


# search-url http://wanted-pedo.com/bis/page/0/?s=var
base_url = 'http://wanted-pedo.com/bis/'
search_url = 'page/{page}/?s={query}'

results_xpath = '//div[@id="blog-item-holder"]/div[@class="row"]/div[@class="six columns gdl-blog-widget"]'
url_xpath = './/h2[@class="blog-title"]/a/@href'
title_xpath = './/h2[@class="blog-title"]/a//text()'
content_xpath = './/div[@class="blog-content"]//text()'
thumbnail_xpath = './/div[@class="blog-media-wrapper gdl-image"]/a/img/@src'
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
            logger.exception('Erreur: wanted-pedo')
            continue

        results.append(res)

    return results
