# -*- coding: utf-8 -*-
import os
import re
import math
from eol_spider.items import GooglePublicationItem, GoogleArticlesItem
from eol_spider.datafilter import DataFilter
from eol_spider.mysql_utils import MYSQLUtils
from eol_spider.settings import mysql_connection
from eol_spider.func import mysql_datetime, get_google_spider_url

from scrapy.spiders import CrawlSpider
from scrapy import Request


class GoogleScholarSpider(CrawlSpider):
    name = 'GoogleScholarSpider'
    # custom_settings = {
    #     'DOWNLOAD_DELAY': '4.1',
    # }
    domain = 'https://scholar.google.co.jp'
    #location.replace('http://pubs.acs.org/doi/abs/10.1021/ac202028g')
    article_link_pattern = re.compile(r"0;url=(.*)$")

    def start_requests(self):
        cate_list = MYSQLUtils.fetch_cate_list(self)
        # yield Request("http://www.baidu.com", callback=self.parse)
        for cate in cate_list:
            meta = {
                "cate1_id": cate['fid'],
                "cate2_id": cate['cate_id']
            }
            cate_url = get_google_spider_url(cate['cate_url'])
            yield Request(cate_url, callback=self.parse, meta=meta)
            #break

    def parse(self, response):
        # print response.body
        # return
        for row in response.xpath('//*[@id="gs_cit_list_table"]/tr[position()>1]'):
            item = GooglePublicationItem()
            item['cate1_id'] = response.meta['cate1_id']
            item['cate2_id'] = response.meta['cate2_id']
            item['name'] = DataFilter.simple_format(row.xpath('td[position()=2]').extract())
            item['desc'] = ''
            item['h5_idx'] = DataFilter.simple_format(row.xpath('td[position()=3]').extract())
            item['h5_med'] = DataFilter.simple_format(row.xpath('td[position()=4]').extract())
            item['rank'] = DataFilter.simple_format(row.xpath('td[position()=1]').extract())
            item['create_time'] = mysql_datetime()
            article_list_url = "%s%s" % (self.domain,
                                         DataFilter.simple_format(row.xpath('td[position()=3]/a/@href').extract()))
            publication_id = MYSQLUtils.save(self, "google_publication", item)[0]
            response.meta['publication_id'] = publication_id
            response.meta['h5_idx'] = item['h5_idx']
            yield Request(article_list_url, callback=self.parse_article_list, meta=response.meta)
            #break

    def parse_article_list(self, response):
        page_size = 20
        h5_idx = response.meta['h5_idx']
        page_count = int(math.ceil(int(h5_idx) / page_size))
        for page_number in range(1, page_count + 1):
            cstart = (page_number - 1) * page_size
            url = DataFilter.add_url_parameter(response.url, "cstart=%d" % cstart)
            yield Request(url, callback=self.parse_article, meta=response.meta)
            #break

    def parse_article(self, response):
        for row in response.xpath('//*[@id="gs_cit_list_table"]/tr[position()>1]'):
            article_selector = row.xpath('td[position()=1]')
            ref_selector = row.xpath('td[position()=2]')
            response.meta['publication_id'] = response.meta['publication_id']
            response.meta['cate1_id'] = response.meta['cate1_id']
            response.meta['cate2_id'] = response.meta['cate2_id']
            response.meta['article_title'] = DataFilter.simple_format(
                article_selector.xpath('descendant::span[1]').extract())
            response.meta['article_link'] = DataFilter.simple_format(
                article_selector.xpath('descendant::a/@href').extract())
            response.meta['article_authors'] = DataFilter.simple_format(
                article_selector.xpath('descendant::span[2]').extract())
            response.meta['publish_info'] = DataFilter.simple_format(
                article_selector.xpath('descendant::span[3]').extract())
            response.meta['ref_link'] = "%s%s" % (self.domain,
                                                  DataFilter.simple_format(
                                                      ref_selector.xpath('descendant::a/@href').extract()))
            response.meta['ref_count'] = DataFilter.simple_format(ref_selector.xpath('descendant::a').extract())
            response.meta['publish_date'] = DataFilter.simple_format(row.xpath('td[position()=3]').extract())
            response.meta['create_time'] = mysql_datetime()
            yield Request(response.meta['article_link'], callback=self.insert_article, meta=response.meta)
            #break

    def insert_article(self, response):
        article_link = response.url
        content = DataFilter.simple_format(response.xpath('//meta[@http-equiv="refresh"]/@content').extract())
        article_link_match = re.search(self.article_link_pattern, content)
        if article_link_match:
            article_link = article_link_match.group(1)
        item = GoogleArticlesItem()
        for key in MYSQLUtils.get_columns_by_item(item):
            item[key] = response.meta[key]
        item['article_link'] = article_link
        article_id = MYSQLUtils.save(self, "google_articles", item)[0]
        response.meta['article_id'] = article_id

    def close(self, reason):
        self.db.close()
        super(GoogleScholarSpider, self).close(self, reason)

    def __init__(self, mode=None, **kwargs):
        self.db = mysql_connection
        self.mode = mode
        if mode == "init":
            os.system("scrapy crawl GoogleScholarCategorySpider")
        MYSQLUtils.cleanup_google_publication_articles(self)
        super(GoogleScholarSpider, self).__init__(**kwargs)
        pass
