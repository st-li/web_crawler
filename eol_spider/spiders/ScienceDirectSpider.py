# -*- coding: utf-8 -*-
import math
from eol_spider.items import GooglePublicationItem, GoogleArticlesItem, GoogleAuthorsItem, GoogleAffiliationItem
from eol_spider.datafilter import DataFilter
from eol_spider.mysql_utils import MYSQLUtils
from eol_spider.settings import mysql_connection
from eol_spider.func import mysql_datetime

from scrapy.spiders import CrawlSpider
from scrapy import Request


class ScienceDirectSpider(CrawlSpider):
    name = 'ScienceDirectSpider'
    domain = 'http://www.sciencedirect.com'

    def start_requests(self):
        article_list = MYSQLUtils.fetch_article_list(self, self.domain)
        # print article_list[0]
        for article in article_list:
            meta = {}
            url = article['article_link']
            for key in article.keys():
                meta[key] = article[key]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
            }
            yield Request(url, callback=self.parse, meta=meta, headers=headers)
            #break

    def parse(self, response):

        author_items = []
        for author in response.xpath('//*[contains(@class, "authorName")]'):
            author_item = GoogleAuthorsItem()
            author_item['publication_id'] = response.meta['publication_id']
            author_item['article_id'] = response.meta['article_id']
            author_item['affiliation_id'] = ''
            author_item['fullname'] = DataFilter.simple_format(author.xpath('.').extract())
            author_item['create_time'] = mysql_datetime()
            author_items.append(author_item)

        affiliation_items = []
        for affiliation in response.xpath('//*[contains(@class, "affiliation")]'):
            affiliation_item = GoogleAffiliationItem()
            affiliation_item['publication_id'] = response.meta['publication_id']
            affiliation_item['article_id'] = response.meta['article_id']
            affiliation_item['desc'] = DataFilter.simple_format(affiliation.xpath('.').extract())
            affiliation_item['create_time'] = mysql_datetime()
            affiliation_items.append(affiliation_item)

        MYSQLUtils.save(self, "google_authors", author_items)
        MYSQLUtils.save(self, "google_affiliations", affiliation_items)

    def close(self, reason):
        self.db.close()
        super(ScienceDirectSpider, self).close(self, reason)

    def __init__(self, mode=None, **kwargs):
        self.db = mysql_connection
        MYSQLUtils.cleanup_google_author_affiliations(self, self.domain)
        super(ScienceDirectSpider, self).__init__(**kwargs)
        pass
