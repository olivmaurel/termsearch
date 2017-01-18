import json
import logging

import scrapy

from aggregator.scraper.items import RecordLoader, Record
from aggregator.scraper.spidersold.iate import logger
from aggregator.scraper.spidersold.proz import logger

logger = logging.getLogger(__name__)


class GenericSpider(scrapy.Spider):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.source_language = source_language
        self.target_language = target_language


    def __str__(self):
        return "URL: {}\n Keywords: {}\n Langpair {}/{}".format(self.start_urls, self.keywords, self.source_language, self.target_language)


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

            rec.add_value('domain', self.get_domains(text))

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



    def get_domains(self, result):
        """
        truncate the unnecessary part at the end of the domain string
        by deleting everything starting from the [ character (and -1 for the extra whitespace)
        returns a list of strings
        # >>> get_domains(['TECHNICAL, AGRICULTURE, FORESTRY AND FISHERIES [EP] Full entry'])
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


class ProzSpider(GenericSpider):

    name = 'proz'

    def __init__(self, keywords, source_language, target_language, *args,  **kwargs):

        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # proz uses 3 digits language codes 'eng', 'fra, 'ita' etc
        self.source_language = source_language.code3d
        self.target_language = target_language.code3d
        self.remoteurl = 'http://www.proz.com/ajax/ajax_search.php'
        self.start_urls = [self.remoteurl]

    def parse(self, response):

        formdata = {'action': 'term_search',
                    'search_params[term]': self.keywords,
                    'search_params[from]': self.source_language,
                    'search_params[to]': self.target_language,
                    'search_params[bidirectional]': 'true',
                    'search_params[results_per_page]': '100'}

        return scrapy.FormRequest(
            url= self.remoteurl,
            formdata=formdata,
            callback=self.get_records
        ) # todo add errback to deal with the different HTTP errors returned by the crawler

    def get_records(self,response):
        # all the results tables are contained within 1 value in a json file,
        # so we need to create a new selector with the html within the json
        selector = scrapy.Selector(text=json.loads(response.text)['html'],
                                   type='html')
        # tables are the different results to parse
        tables = selector.xpath('//tbody[@class=\'search_result_body\']/tr/td[4]')
        logger.debug("found {} results".format(len(tables)))
        # for each result
        for i, result in enumerate(tables):

            domain = result.xpath('normalize-space(string(../td[3]))').extract()
            terms = result.xpath('normalize-space(string(./a))').extract()
            translations = result.xpath('normalize-space(string(./a[2]))').extract()
            logger.debug([domain, terms, translations])

            # create a new record
            rec = RecordLoader(Record(), selector=result)
            rec.add_value('website', self.name)
            rec.add_value('domain', domain),
            rec.add_value('source_language',self.source_language),
            rec.add_value('target_language', self.target_language),
            rec.add_value('terms', terms),
            rec.add_value('translations', translations),


            yield rec.load_item()

class TermiumSpider (GenericSpider):

    name = 'termium'

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(keywords, source_language, target_language, *args, **kwargs)
        # 'keywords' inherited from GenericSpider
        # proz uses 2 digits language codes 'en', 'fr, 'it' etc
        self.source_language = source_language.code2d
        self.target_language = target_language.code2d

        self.remoteurl = 'http://www.btb.termiumplus.gc.ca/tpv2alpha/' \
                         'alpha-eng.html?lang=eng&srchtxt={}'.format(keywords)


        self.start_urls = [self.remoteurl]

    def parse (self, response):
        logger.debug(response)

        tables = response.xpath('//div[@id=\'resultrecs\']/'
                                'section[contains(normalize-space(@class), \'recordSet\')]/div')
        logger.debug(tables)
        logger.debug('Found {} results on {}'.format(len(tables), self.name))

        logger.debug(tables)
        results = []
        for record in (tables):
            logger.info(record)
            # create a new record
            rec = RecordLoader(Record(), selector=record)
            rec.add_value('website', self.name)
            rec.add_value('domain', self.get_domains(record)),
            rec.add_value('source_language',self.source_language),
            rec.add_value('target_language', self.target_language),
            rec.add_value('terms', self.get_terms(record, self.source_language)),
            rec.add_value('translations', self.get_terms(record, self.target_language)),

            logger.info(rec)

            results.append(record)

            yield rec.load_item()

    def get_domains(self, record):
        '''
        :param record: a SelectorList from main results table ('tables' in parse() )
        :return: a list of strings of every dom  ain included in the record
        '''
        return record.xpath('div[@class=\'col-md-4\']/section/div/section[@lang=\'en\']'
                            '/div/ul//li[@class=\'small\']'
                            ).xpath('normalize-space(.)').extract()

    def get_terms(self, record, language):

        results_list = []

        # clean up the useless content, everything from " \xa0" on should be removed
        for result in record.xpath('div[@class=\'col-md-4\']/section/div/div[@lang=\'{}\']/ul'
                              '/li[contains(@class,\'text-primary\')]'.format(language)
                              ).xpath('normalize-space(.)').extract():

            results_list.append(result[:result.index('\xa0')-1])

        return results_list
