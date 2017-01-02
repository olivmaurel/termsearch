# -*- coding: utf-8 -*-
import json

import scrapy

try:
    from .generic import GenericSpider
except ImportError:
    from scraper.spiders.generic import GenericSpider
try:
    from aggregator.scraper import Record, RecordLoader
except ImportError:
    from scraper.items import Record, RecordLoader


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class ProzSpider(GenericSpider):

    name='proz'

    def __init__(self, keywords, source_language, target_language, *args,  **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # proz uses 3 digits language codes 'eng', 'fra, 'ita' etc
        self.source_language = source_language.code3d
        self.target_language = target_language.code3d

        self.remoteurl = 'http://www.proz.com/ajax/ajax_search.php'



        self.start_urls = [self.remoteurl]

    def parse(self, response):

        logger.debug(self)
        print(self)

        formdata = {'action': 'term_search',
                    'search_params[term]': self.keywords,
                    'search_params[from]': self.source_language,
                    'search_params[to]': self.target_language,
                    'search_params[bidirectional]': 'true',
                    'search_params[results_per_page]': '100'}

        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.get_records
        )

    def get_records(self,response):

        selector = scrapy.Selector(text=json.loads(response.text),
                                   type='html')

        tables = selector.xpath('//tbody[@class=\'search_result_body\']/tr/td[4]')

        for i, result in enumerate(tables):

            rec = RecordLoader(Record(), result)
            rec.add_value('website', self.name)
            rec.add_value('domain', result.xpath('normalize-space(string(../td[3]))')),
            rec.add_value('source_language',self.source_language),
            rec.add_value('target_language', self.target_language),
            rec.add_value('terms', result.xpath('normalize-space(string(./a))')),
            rec.add_value('target', e.xpath('normalize-space(string(./a[2]))')),

            yield rec.load_item()

if __name__ == "__main__":
    from aggregator.models import *
    import scrapydo

    scrapydo.setup()

    search_parameters={'keywords':'boilerplate',
                   'source_language': Language.objects.get('en'),
                   'target_language': Language.objects.get('fr')}

    spider = scrapydo.run_spider(ProzSpider(**search_parameters), **search_parameters)
    print(spider)