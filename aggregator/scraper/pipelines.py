# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class TermscraperPipeline(object):

    char_limit = 100

    def process_item(self, item, spider):

        text_input_to_check = [item['terms'], item['translations']]

        for text_input in text_input_to_check:
            if text_input >= self.char_limit:
                raise DropItem('There is a string longer than {}, drop this item'.format(self.char_limit))
            if len(text_input) == 0:
                raise DropItem('One of the text fields is empty, drop this item')

        # if we get out of the loop, all the sanity checks are OK
        return item
