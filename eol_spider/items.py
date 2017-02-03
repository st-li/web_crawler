# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CandidateBasicItem(Item):
    # define the fields for your item here like:
    # name = Field()
    country_id = Field()
    college_id = Field()
    discipline_id = Field()
    fullname = Field()
    academic_title = Field()
    other_title = Field()
    nationality = Field()
    email = Field()
    phonenumber = Field()
    external_link = Field()
    experience = Field()
    desc = Field()
    extra = Field()
    avatar_url = Field()
    discipline_desc = Field()
    create_time = Field()


class CandidateEducationItem(Item):
    cb_id = Field()
    college = Field()
    discipline = Field()
    start_time = Field()
    end_time = Field()
    duration = Field()
    degree = Field()
    desc = Field()
    create_time = Field()


class CandidateResearchItem(Item):
    cb_id = Field()
    interests = Field()
    current_research = Field()
    research_summary = Field()
    create_time = Field()


class CandidatePublicationsItem(Item):
    cb_id = Field()
    publications = Field()
    create_time = Field()


class CandidateCoursesItem(Item):
    cb_id = Field()
    courses_no = Field()
    courses_desc = Field()
    create_time = Field()


class CandidateWorkexperienceItem(Item):
    cw_id = Field()
    cb_id = Field()
    job_title = Field()
    company = Field()
    start_time = Field()
    end_time = Field()
    duration = Field()
    desc = Field()
    create_time = Field()


class GoogleCategoryItem(Item):
    fid = Field()
    name = Field()
    cate_url = Field()
    create_time = Field()


class GooglePublicationItem(Item):
    cate1_id = Field()
    cate2_id = Field()
    name = Field()
    desc = Field()
    h5_idx = Field()
    h5_med = Field()
    rank = Field()
    create_time = Field()


class GoogleArticlesItem(Item):
    publication_id = Field()
    cate1_id = Field()
    cate2_id = Field()
    article_title = Field()
    article_link = Field()
    article_authors = Field()
    publish_info = Field()
    ref_link = Field()
    ref_count = Field()
    publish_date = Field()
    create_time = Field()


class GoogleAuthorsItem(Item):
    publication_id = Field()
    article_id = Field()
    affiliation_id = Field()
    fullname = Field()
    create_time = Field()


class GoogleAffiliationItem(Item):
    publication_id = Field()
    article_id = Field()
    desc = Field()
    create_time = Field()