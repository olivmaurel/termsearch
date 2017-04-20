from aggregator.models import Language
from aggregator.scraper.mytestspiders import *
import requests

def iate_tester():

    search_parameters = {'keywords': 'boilerplate',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}
    spider = IateSpider(**search_parameters)

    response = requests.get(spider.url)
    return spider.get_results_as_list(response)


def proz_tester():

    search_parameters = {'keywords': 'boilerplate',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    spider = ProzSpider(**search_parameters)

    response = requests.post(spider.url, data=spider.formdata)

    return spider.get_results_as_list(response)