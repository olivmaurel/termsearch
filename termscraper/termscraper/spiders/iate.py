# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.loader import ItemLoader
from termscraper.items import Record, RecordLoader




class IateSpider(scrapy.Spider):
    name = 'iate'
    search_keywords = 'computer' # dg connect
    sourceLanguage = 'en'
    targetLanguage = 'fr'
    remoteurl = 'http://iate.europa.eu/SearchByQuery.do?method=search&query={}&sourceLanguage={}&targetLanguages={}&domain=0&matching=&typeOfSearch=s'.format(search_keywords, sourceLanguage, targetLanguage)    
    start_urls = [remoteurl]

    def parse(self, response):
        
        tables = response.xpath('//div[@id="searchResultBody"]/table')

        for i, table in enumerate(tables):
            
            result = table.xpath('./tr')
            text = result.xpath('normalize-space(.)')
            rec = RecordLoader(Record(), text)
            
            rec.add_value('last_updated', datetime.date.today())
            rec.add_value('website', self.name)
            rec.add_value('sourceLanguage', self.sourceLanguage)
            rec.add_value('targetLanguage', self.targetLanguage)

            rec.add_value('domain', self.getDomain(text))

            rec.add_value('terms', self.getTerms(text))
            rec.add_value('translations', self.getTranslations(text))

            yield rec.load_item()

        # crawl the next page if more than 10 results
        for f in response.xpath('//div[@id="searchResultFooter"]//*'):
            res = f.xpath('normalize-space(.)').extract()
            if res == ['>']:
                # todo
                next_page = ''.join(f.xpath('./@href').extract())
                yield scrapy.Request(next_page, self.parse)


        # todo: crawl every page when more than 10 results

            
            
    def getDomain(self, result):
        '''truncate the unnecessary part at the end of the domain string
            by deleting everything starting from the [ character (and -1 for the extra whitespace)

        >>> getDomain(['AGRICULTURE, FORESTRY AND FISHERIES [EP] Full entry'])
        'AGRICULTURE, FORESTRY AND FISHERIES'

        '''
        domain = result[0].extract()

        return domain[:domain.index('[')-1]

    def getTerms(self, result):
        
        # the [0] itam is always the domain in the IATE result table
        # the [1] item is always a source in the IATE result table
        # truncate the "EN " at the beginning of the string and add to the list
        terms = [result[1].extract()[3:]]

        # then loop through all the remaining <tr> tags in the table, starting from [2]
        for item in result[2:]:

            item = item.extract()
            
            if item[0:3] == self.targetLanguage.upper()+" ":
                # if the string starts with targetLanguage, then stop and return the result
                return terms
            else:
                terms.append(item)

        return terms

    def getTranslations(self, result):
       
        # the [0] itam is always the domain in the IATE result table
        # the [1] item is always a source in the IATE result table
        # then loop through all the remaining <tr> tags in the table, starting from [2]
        terms = []
        isTranslation = False

        for item in result[2:]:

            item = item.extract()
            
            if item[0:3] == self.targetLanguage.upper()+" ":
                # if the string starts with targetLanguage, insert it after truncating the first 3 characters
                terms.append(item[3:])
                isTranslation = True

            elif isTranslation:
                terms.append(item)

            else:    
                pass

        return terms    


