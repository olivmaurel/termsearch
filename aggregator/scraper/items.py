# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

class Record(scrapy.Item):
    
    terms = scrapy.Field()
    translations = scrapy.Field()
    source_language = scrapy.Field()
    target_language = scrapy.Field()
    domain = scrapy.Field()
    website = scrapy.Field()




class RecordLoader(ItemLoader):

    def strip_tags(x):
        import re

        x = re.sub(re.escape('\xa0'), '', x)

        return x
    
    terms_in = MapCompose(strip_tags)
    
    translations_in = MapCompose(strip_tags)

    
    
