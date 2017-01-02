# -*- coding: utf-8 -*-
import scrapy
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GenericSpider(scrapy.Spider):

    def __init__(self, keywords, source_language, target_language, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords
        self.source_language = source_language
        self.target_language = target_language


    def __str__(self):
        return "URL: {}\n Keywords: {}\n Langpair {}/{}".format(self.start_urls, self.keywords, self.source_language, self.target_language)
