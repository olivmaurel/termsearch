from aggregator.models import Language
from aggregator.scraper.mytestspiders import *
import requests

test_keyword = 'computer'

def iate_tester():

    search_parameters = {'keywords': test_keyword,
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}
    spider = IateSpider(**search_parameters)

    response = requests.get(spider.url)
    return spider.get_results_as_list(response)


def proz_tester():

    search_parameters = {'keywords': test_keyword,
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    spider = ProzSpider(**search_parameters)

    response = requests.post(spider.url, data=spider.formdata)

    return spider.get_results_as_list(response)


def termium_tester():

    search_parameters = {'keywords': test_keyword,
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    spider = TermiumSpider(**search_parameters)

    response = requests.get(spider.url)

    return spider.get_results_as_list(response)


def streamer_tester():

    from itertools import chain

    search_parameters = {'keywords': 'computer',
                         'source_language': Language.objects.get(code2d='en'),
                         'target_language': Language.objects.get(code2d='fr')}

    proz = ProzSpider(**search_parameters)

    return proz.parse(requests.get(proz.url))