# -*- coding: utf-8 -*-
from eol_spider.items import CandidateBasicItem, CandidateCoursesItem, CandidateEducationItem, \
    CandidatePublicationsItem, CandidateResearchItem, CandidateWorkexperienceItem
from eol_spider.datafilter import DataFilter
from eol_spider.mysql_utils import MYSQLUtils
from eol_spider.settings import mysql_connection
from eol_spider.func import mysql_datetime, parse_text_by_multi_content

from scrapy.spiders import CrawlSpider
from scrapy import Request


class ComputerScienceOfWaterLooSpider(CrawlSpider):
    name = 'ComputerScienceOfWaterLooSpider'
    college_name = 'WaterLoo'
    college_id = '2'
    country_id = '2'
    state_id = '2'
    city_id = '2'
    allowed_domains = ['cs.uwaterloo.ca']
    domain = 'https://cs.uwaterloo.ca'
    start_urls = [
        'https://cs.uwaterloo.ca/about/people/group/'
    ]

    def parse(self, response):
        # return
        i = 0
        for staff in response.xpath(
                '//div[contains(@class, "staff-contact")]'):
            cb_items = self.parse_candidate_basic_item(staff)
            cb_id = MYSQLUtils.save(self, "candidate_basic", cb_items)[0]
            staff_profile_url = self.parse_staff_profile_url(staff)
            if staff_profile_url:
                print staff_profile_url
                yield Request(staff_profile_url, callback=self.parse_staff_profile, meta={"cb_id": cb_id})
                pass
                print cb_id
            #i += 1
            #if i > 4:
            #    break

    def parse_staff_profile_url(self, staff):
        profile = DataFilter.simple_format(
            staff.xpath(
                'descendant::div[contains(@class, "field-name-field-contact-profile-url")]/descendant::a/@href').extract())
        return profile
        pass

    def parse_staff_profile(self, response):
        cb_id = response.meta['cb_id']
        summary = response.xpath('//div[contains(@class, "field-type-text-with-summary")]')

        ce_items = self.parse_candidate_education_item(summary, cb_id)
        MYSQLUtils.save(self, "candidate_education", ce_items)

        cr_items = self.parse_candidate_research_item(summary, cb_id)
        MYSQLUtils.save(self, "candidate_research", cr_items)
        #
        cp_items = self.parse_candidate_publications_item(summary, cb_id)
        MYSQLUtils.save(self, "candidate_publications", cp_items)
        #
        cc_items = self.parse_candidate_courses_item(summary, cb_id)
        MYSQLUtils.save(self, "candidate_courses", cc_items)
        #
        cw_items = self.parse_candidate_workexperience_item(summary, cb_id)
        MYSQLUtils.save(self, "candidate_workexperience", cw_items)
        pass

    def parse_content(self, summary, head_str):
        is_end = False
        next_h2 = summary.xpath('descendant::h2[text()="%s"]/following-sibling::h2[1]' % head_str)
        if not next_h2:
            is_end = True
        if is_end:
            content = summary.xpath('descendant::h2[text()="%s"]/following-sibling::p' % head_str)
        else:
            next_h2_txt = DataFilter.simple_format(next_h2.extract())
            content = summary.xpath(
                'descendant::p[preceding-sibling::h2/text()="%s" and following-sibling::h2/text()="%s"]'
                % (head_str, next_h2_txt))
        print content
        # summary.xpath('descendant::p[preceding-sibling::h2/text()='%s' and following-sibling::h2/@property='p2']')
        return content

        pass

    def parse_candidate_basic_item(self, staff):
        items = []
        item = CandidateBasicItem()
        item['country_id'] = self.country_id
        item['college_id'] = self.college_id
        item['discipline_id'] = '0'
        item['fullname'] = DataFilter.simple_format(
            staff.xpath('descendant::*[@property="schema:name"]').extract())
        item['academic_title'] = DataFilter.simple_format(
            staff.xpath('descendant::*[@property="schema:jobTitle"]').extract())
        item['other_title'] = ''
        item['nationality'] = ''
        item['email'] = DataFilter.simple_format(
            staff.xpath('descendant::*[@property="schema:email"]').extract())
        item['phonenumber'] = DataFilter.simple_format(
            staff.xpath('descendant::*[@property="schema:telephone"]').extract())
        item['external_link'] = DataFilter.simple_format(
            staff.xpath(
                'descendant::*[contains(@class, "field-name-field-contact-website-url")]\
                /descendant::a/@href').extract())
        item['experience'] = ''
        item['desc'] = ''
        item['avatar_url'] = DataFilter.simple_format(
            staff.xpath(
                'descendant::*[contains(@class, "field-name-field-contact-image")]\
                /descendant::img/@src').extract())
        item['create_time'] = mysql_datetime()
        location = DataFilter.simple_format(
            staff.xpath('descendant::*[@property="schema:workLocation"]').extract())
        group = parse_text_by_multi_content(staff.xpath('descendant::*[@rel="schema:affiliation"]'), ",")
        item['extra'] = '{"location": "%s", "group": "%s"}' % (location, group)
        items.append(item)
        print items
        return items
        pass

    def parse_candidate_education_item(self, summary, cb_id):
        now_time = mysql_datetime()
        items = []
        desc = self.parse_content(summary, "Degrees and Awards")
        item = CandidateEducationItem()
        item['cb_id'] = cb_id
        item['college'] = ''
        item['discipline'] = ''
        item['start_time'] = ''
        item['end_time'] = ''
        item['duration'] = ''
        item['degree'] = ''
        item['desc'] = parse_text_by_multi_content(desc, "\n")
        item['create_time'] = now_time
        items.append(item)
        print items
        return items
        pass

    def parse_candidate_research_item(self, summary, cb_id):
        now_time = mysql_datetime()
        items = []
        item = CandidateResearchItem()
        item['cb_id'] = cb_id
        interests = self.parse_content(summary, "Research Interests")
        item['interests'] = parse_text_by_multi_content(interests, "\n")
        item['current_research'] = ''
        item['research_summary'] = ''
        item['create_time'] = now_time
        items.append(item)
        print items
        return items

        pass

    def parse_candidate_publications_item(self, summary, cb_id):
        now_time = mysql_datetime()
        items = []
        pub_items = self.parse_content(summary, "Representative Publications")
        for pub_item in pub_items:
            item = CandidatePublicationsItem()
            # 斯坦福大学无法直接获取到教育经历的相关字段，因此只有desc字段有值，其他字段留待后续分析处理
            item['cb_id'] = cb_id
            item['publications'] = DataFilter.simple_format(pub_item.xpath('.').extract())
            if not item['publications']:
                continue
            item['create_time'] = now_time
            items.append(item)
        print items
        return items
        pass

    def parse_candidate_courses_item(self, summary, cb_id):
        return []
        pass

    def parse_candidate_workexperience_item(self, summary, cb_id):
        now_time = mysql_datetime()
        items = []
        desc = self.parse_content(summary, "Industrial and Sabbatical Experience")
        item = CandidateWorkexperienceItem()
        item['cb_id'] = cb_id
        item['job_title'] = ''
        item['company'] = ''
        item['start_time'] = ''
        item['end_time'] = ''
        item['duration'] = ''
        item['desc'] = parse_text_by_multi_content(desc, "\n")
        item['create_time'] = now_time
        items.append(item)
        print items
        return items
        pass

    def close(self, reason):
        self.db.close()
        super(ComputerScienceOfWaterLooSpider, self).close(self, reason)

    def __init__(self, **kwargs):
        self.db = mysql_connection
        MYSQLUtils.cleanup_data(self)
        super(ComputerScienceOfWaterLooSpider, self).__init__(**kwargs)
        pass
