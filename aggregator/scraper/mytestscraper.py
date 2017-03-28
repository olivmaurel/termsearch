import requests
from lxml import html



def launchit():

    from aggregator.scraper.spiders import IateSpider
    from aggregator.models import Language

    search_parameters = {'keywords': 'boilerplate',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    spider = IateSpider(**search_parameters)

    r = requests.get(spider.remoteurl)
    tree = html.fromstring(r.text)



    return spider.parse(tree)