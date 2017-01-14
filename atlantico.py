"""
 atlantico (Web)

 @website     http://atlantico.fr
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

logger = logger.getChild('atlantico')

# engine dependent config
categories = ['information', 'general']
paging = True


# search-url http://www.atlantico.fr/search/site/var/page/0/0
base_url = 'http://www.atlantico.fr'
search_url = '/search/site/{query}/page/{page}/0'

results_xpath = '//ul[@class="list"]/li[@class="content"]'
url_xpath = './/h2[@class="s2"]/a/@href'
title_xpath = './/h2[@class="s2"]/a//text()'
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
            res = {'url': base_url + result.xpath(url_xpath)[0],
                   'title': escape(''.join(result.xpath(title_xpath))),
                   'content': escape(''.join(result.xpath(content_xpath)))}
        except:
            logger.exception('Erreur: atlantico')
            continue

        results.append(res)

    return results
