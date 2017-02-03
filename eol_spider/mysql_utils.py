# -*- coding: utf-8 -*-
from __future__ import division
import logging


class MYSQLUtils(object):
    @staticmethod
    def fetch_result(db, query_sql, maxrows=0, how=1):
        db.query(query_sql)
        r = db.store_result()
        return r.fetch_row(maxrows, how)

    @staticmethod
    def build_insert_sql(table, items):
        if not isinstance(items, list):
            items = [items]
        values_sql = ''
        # add by steven
        for item in items:
            print item;
        # add by steven(end)
        columns = MYSQLUtils.get_columns_by_item(items[0])

        column_sql = ''
        for column in columns:
            column_sql = "%s`%s`," % (column_sql, column)
        column_sql = column_sql[:-1]
        # print column_sql
        for item in items:
            value_sql = ''
            for column in columns:
                value_sql = "%s'%s'," % (value_sql, item.get(column))
            value_sql = value_sql[:-1]

            values_sql = "%s(%s)," % (values_sql, value_sql)
            pass
        values_sql = values_sql[:-1]
        # print values_sql
        insert_sql = "INSERT INTO `%s` (%s) VALUES %s" % (table, column_sql, values_sql)
        # print insert_sql
        return insert_sql

    @staticmethod
    def get_columns_by_item(item):
        item_dict = item.__class__.__dict__
        fields = item_dict['fields'].keys()
        return fields

    @staticmethod
    def save(spider, table, items):
        if len(items) == 0 or not items:
            return 0
        db = spider.db
        insert_sql = MYSQLUtils.build_insert_sql(table, items)
        #print insert_sql
        db.query(insert_sql)
        insert_id = db.insert_id()
        affected_rows = db.affected_rows()
        return insert_id, affected_rows

    @staticmethod
    def cleanup_associate(spider, source_table, target_table, pk_column, join_column, where):
        cleanup_associate_sql = MYSQLUtils.build_cleanup_associate_sql(source_table, target_table, pk_column,
                                                                       join_column, where)
        #print cleanup_associate_sql
        db = spider.db
        db.query(cleanup_associate_sql)
        affected_rows = db.affected_rows()
        logging.info("remove %s lines from table %s that associate with table %s!" %
                     (affected_rows, target_table, source_table))
        return affected_rows
        pass

    @staticmethod
    def build_cleanup_associate_sql(source_table, target_table, pk_column, join_column, where):
        # sample sql statement:
        # delete from `candidate_courses` where `cc_id` IN
        # (select tmp.`cc_id` from (
        # select cc.`cc_id` from `candidate_courses` cc
        # left join `candidate_basic` cb on cb.`cb_id`=cc.`cb_id`
        # where cb.`college_id`='1'
        # ) tmp

        cleanup_associate_sql = "delete from `%s` where `%s` IN \
                            (select tmp.`%s` from ( \
                              select target.`%s` from `%s` target " \
                                "left join `%s` source on source.`%s`=target.`%s` " \
                                "where %s\
                                ) tmp\
                                )" % (target_table, pk_column, pk_column, pk_column, target_table, source_table,
                                      join_column, join_column, where)
        # print cleanup_associate_sql
        return cleanup_associate_sql
        pass

    @staticmethod
    def cleanup(spider, table, where):
        cleanup_sql = MYSQLUtils.build_cleanup_sql(table, where)
        db = spider.db
        db.query(cleanup_sql)
        affected_rows = db.affected_rows()
        logging.info("remove %s lines from table %s!" %
                     (affected_rows, table))
        return affected_rows

    @staticmethod
    def build_cleanup_sql(table, where):
        # sample sql statement:
        # delete from `candidate_basic` where `college_id`='2'

        cleanup_sql = "delete from `%s` where %s" % (table, where)
        # print cleanup_sql
        return cleanup_sql
        pass

    @staticmethod
    def cleanup_data(spider):
        logging.info("doing cleanup jobs!")
        MYSQLUtils.cleanup_associate(spider, "candidate_basic", "candidate_education", "ce_id", "cb_id",
                                     "%s.`%s`='%s'" % ("source", "college_id", spider.college_id))
        MYSQLUtils.cleanup_associate(spider, "candidate_basic", "candidate_research", "cr_id", "cb_id",
                                     "%s.`%s`='%s'" % ("source", "college_id", spider.college_id))
        MYSQLUtils.cleanup_associate(spider, "candidate_basic", "candidate_publications", "cp_id", "cb_id",
                                     "%s.`%s`='%s'" % ("source", "college_id", spider.college_id))
        MYSQLUtils.cleanup_associate(spider, "candidate_basic", "candidate_courses", "cc_id", "cb_id",
                                     "%s.`%s`='%s'" % ("source", "college_id", spider.college_id))
        MYSQLUtils.cleanup_associate(spider, "candidate_basic", "candidate_workexperience", "cw_id", "cb_id",
                                     "%s.`%s`='%s'" % ("source", "college_id", spider.college_id))
        MYSQLUtils.cleanup(spider, "candidate_basic", "`college_id`='%s'" % spider.college_id)
        pass

    @staticmethod
    def cleanup_google_category(spider):
        logging.info("doing cleanup google_category jobs!")
        MYSQLUtils.truncate(spider, "google_category")

    @staticmethod
    def cleanup_google_publication_articles(spider):
        logging.info("doing cleanup google_publication and google_articles jobs!")
        MYSQLUtils.truncate(spider, "google_publication")
        MYSQLUtils.truncate(spider, "google_articles")

    @staticmethod
    def cleanup_google_author_affiliations(spider, domain):
        logging.info("doing cleanup google_author and google_affiliations jobs!")
        length = len(domain)
        where = "LEFT(%s.`article_link`, %d)='%s'" \
                % ("source", length, domain)
        MYSQLUtils.cleanup_associate(spider, "google_articles", "google_authors", "author_id", "article_id",
                                     where)
        MYSQLUtils.cleanup_associate(spider, "google_articles", "google_affiliations", "affiliation_id", "article_id",
                                     where)

    @staticmethod
    def truncate(spider, table):
        db = spider.db
        truncate_sql = "TRUNCATE TABLE `%s`" % table
        logging.info(truncate_sql)
        db.query(truncate_sql)

    @staticmethod
    def fetch_cate_list(spider):
        db = spider.db
        query_sql = "SELECT `cate_id`,`fid`,`name`,`cate_url` FROM `google_category` WHERE fid!=0"
        cate_list = MYSQLUtils.fetch_result(db, query_sql)
        return cate_list

    @staticmethod
    def fetch_article_list(spider, domain):
        length = len(domain)
        db = spider.db
        query_sql = "SELECT \
                    `article_id`,\
                    `publication_id`,\
                    `cate1_id`,\
                    `cate2_id`,\
                    `article_title`,\
                    `article_link`,\
                    `article_authors`,\
                    `publish_info`,\
                    `ref_link`,\
                    `ref_count`,\
                    `publish_date`,\
                    `create_time`\
                    FROM `google_articles`\
                    WHERE LEFT(`article_link`, %d)='%s'" \
                    % (length, domain)
        #print query_sql
        article_link_list = MYSQLUtils.fetch_result(db, query_sql)
        return article_link_list
