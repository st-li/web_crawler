# -*- coding: utf-8 -*-

from eol_spider.items import GoogleCategoryItem
from eol_spider.datafilter import DataFilter
from eol_spider.mysql_utils import MYSQLUtils
from eol_spider.settings import mysql_connection
from eol_spider.func import mysql_datetime

from scrapy.spiders import CrawlSpider
from scrapy import Request


class GoogleScholarCategorySpider(CrawlSpider):
    name = 'GoogleScholarCategorySpider'
    custom_settings = {
        'DOWNLOAD_DELAY': '5',
    }
    domain = 'https://scholar.google.co.jp'
    start_urls = [
        'https://scholar.google.co.jp/citations?view_op=top_venues&hl=zh-CN'
    ]

    def parse(self, response):
        for a in response.xpath('//*[@id="gs_m_broad"]/descendant::a'):
            cate1_url = "%s%s" % (self.domain, DataFilter.simple_format(a.xpath("./@href").extract()))
            cate1_name = DataFilter.simple_format(a.xpath('.').extract())
            item = GoogleCategoryItem()
            item['fid'] = 0
            item['name'] = cate1_name
            item['cate_url'] = cate1_url
            item['create_time'] = mysql_datetime()
            cate1_id = MYSQLUtils.save(self, "google_category", item)[0]
            yield Request(cate1_url, callback=self.parse_cate2, meta={"cate1_id": cate1_id})
            #break

    def parse_cate2(self, response):
        cate1_id = response.meta['cate1_id']
        items = []
        for a in response.xpath('//*[@id="gs_m_rbs"]/descendant::a'):
            item = GoogleCategoryItem()
            item['fid'] = cate1_id
            item['name'] = DataFilter.simple_format(a.xpath('.').extract())
            item['cate_url'] = "%s%s" % (self.domain, DataFilter.simple_format(a.xpath("./@href").extract()))
            item['create_time'] = mysql_datetime()
            items.append(item)
        MYSQLUtils.save(self, "google_category", items)

    def close(self, reason):
        self.db.close()
        super(GoogleScholarCategorySpider, self).close(self, reason)

    def __init__(self, **kwargs):
        self.db = mysql_connection
        MYSQLUtils.cleanup_google_category(self)
        super(GoogleScholarCategorySpider, self).__init__(**kwargs)
        pass
