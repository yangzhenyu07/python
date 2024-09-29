# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
用于定义我们将爬取的数据结构：
"""


class BaiduHotsItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    # pass
