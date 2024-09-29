import scrapy
from baidu_hots.items import BaiduHotsItem
import pdb  # 导入调试库

from scrapy.spidermiddlewares.httperror import HttpError


class BaiduSpider(scrapy.Spider):
    name = 'baidu_hots'
    allowed_domains = ['top.baidu.com']
    start_urls = ['https://top.baidu.com/board?platform=pc&sa=pcindex_entry']

    def parse(self, response):
        hot_search_items = response.css('div.active-item_1Em2h')
        for item in hot_search_items:
            rank = item.css('div.sign-index_mtI7K::text').get()
            title = item.css('div.c-single-text-ellipsis::text').get()
            # pdb.set_trace()  # 设置断点
            if rank is None or rank.strip() == "":
                continue
            if rank and title:
                baidu_item = BaiduHotsItem()
                baidu_item['rank'] = rank.strip()
                baidu_item['title'] = title.strip()

                yield baidu_item

    def errback_httpbin(self, failure):
        # 错误时进入此处
        self.logger.error(repr(failure))

        # 可以通过 failure 检查异常类型
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HttpError on {response.url}')
