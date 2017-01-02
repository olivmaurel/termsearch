# -*- coding: utf-8 -*-
import scrapy

from .generic import GenericSpider

from aggregator.scraper.items import Record, RecordLoader

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class IateSpider(GenericSpider):

    name='iate'

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # IATE uses 2 digits language codes 'en', 'fr, 'it' etc
        self.source_language = source_language.code2d
        self.target_language = target_language.code2d

        self.remoteurl = 'http://iate.europa.eu/SearchByQuery.do?' \
                    'method=search&query={}&sourceLanguage={}' \
                    '&targetLanguages={}&domain=0' \
                    '&matching=&typeOfSearch=s'.format(self.keywords, self.source_language, self.target_language)

        self.start_urls = [self.remoteurl]


    def parse(self, response):

        logger.debug(self)
        print(self)
        tables = response.xpath('//div[@id="searchResultBody"]/table')


        for i, table in enumerate(tables):
            
            result = table.xpath('./tr')
            text = result.xpath('normalize-space(.)')
            rec = RecordLoader(Record(), text)
            
            # rec.add_value('last_updated', datetime.date.today())
            rec.add_value('website', self.name)
            rec.add_value('source_language', self.source_language)
            rec.add_value('target_language', self.target_language)

            rec.add_value('domain', self.getdomains(text))

            rec.add_value('terms', self.getterms(text))
            rec.add_value('translations', self.gettranslations(text))

            yield rec.load_item()

        # crawl the next page if more than 10 results
        for f in response.xpath('//div[@id="searchResultFooter"]//*'):
            res = f.xpath('normalize-space(.)').extract()
            if res == ['>']:
                # todo: crawl every page when more than 10 pages
                next_page = ''.join(f.xpath('./@href').extract())
                yield scrapy.Request(next_page, self.parse)



    def getdomains(self, result):
        """
        truncate the unnecessary part at the end of the domain string
        by deleting everything starting from the [ character (and -1 for the extra whitespace)
        returns a list of strings
        # >>> getdomains(['TECHNICAL, AGRICULTURE, FORESTRY AND FISHERIES [EP] Full entry'])
        # ['TECHNICAL', 'AGRICULTURE, FORESTRY AND FISHERIES']
        """

        text = result[0].extract()[:result[0].extract().index('[')-1]
        domains = text.split(', ')
        return domains

    def getterms(self, result):
        """
        the [0] item is always the domain in the IATE result table
        the [1] item is always a source in the IATE result table
        truncate the "EN " at the beginning of the string and add to the list
        """
        terms = [result[1].extract()[3:]]

        # then loop through all the remaining <tr> tags in the table, starting from [2]
        for item in result[2:]:

            item = item.extract()
            
            if item[0:3] == self.target_language.upper()+" ":
                # if the string starts with target_language, then stop and return the result
                return terms
            else:
                terms.append(item)

        return terms

    def gettranslations(self, result):
       
        # the [0] itam is always the domain in the IATE result table
        # the [1] item is always a source in the IATE result table
        # then loop through all the remaining <tr> tags in the table, starting from [2]
        terms = []
        is_translation = False

        for item in result[2:]:

            item = item.extract()
            
            if item[0:3] == self.target_language.upper()+" ":
                # if the string starts with target_language, truncate the first 3 characters
                terms.append(item[3:])
                is_translation = True

            elif is_translation:
                terms.append(item)

            else:    
                pass

        return terms