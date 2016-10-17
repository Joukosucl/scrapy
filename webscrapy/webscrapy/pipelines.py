# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class moviePipeline(object):
    def __init__(self):
        dbargs = dict(
             host = '127.0.0.1',
             db = 'sucl',
             user = 'root',
             passwd = 'root',
             charset = 'utf8',
             use_unicode = True
            )
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item

    def insert_into_table(self,conn,item):
        sql = '''
              insert into movie(
                en_name,
                subtitle,
                language,
                file_type,
                country,
                zh_name,
                director,
                movie_time,
                score,
                movie_type,
                resolution,
                main_actor
              ) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              '''
        conn.execute(sql, ( 
                item['en_name'],
                item['subtitle'],
                item['language'],
                item['file_type'],
                item['country'],
                item['zh_name'],
                item['director'],
                item['movie_time'],
                item['score'],
                item['movie_type'],
                item['resolution'],
                item['main_actor'],)
            )
