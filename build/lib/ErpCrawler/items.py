# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
import scrapy


class ErpcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    returnJson = scrapy.Field()
    
    def createOne(returnJson):
        tmp=ErpcrawlerItem()
        tmp['returnJson']=returnJson
        return tmp
