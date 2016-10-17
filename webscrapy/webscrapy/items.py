# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class movieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zh_name = scrapy.Field() # 中文名称
    en_name = scrapy.Field() # 英文名称
    pub_time = scrapy.Field() # 发布时间
    movie_time = scrapy.Field() # 上映时间
    language = scrapy.Field() # 语言
    file_type = scrapy.Field() # 文件类型
    movie_type = scrapy.Field() # 电影类型
    resolution = scrapy.Field()   # 分辨率 
    movie_length = scrapy.Field() # 电影长度(分钟)
    director = scrapy.Field()   # 导演
    main_actor = scrapy.Field() # 主演
    add_time = scrapy.Field()  # 添加时间
    subtitle = scrapy.Field()  # 字幕
    country = scrapy.Field()  # 国家
    score = scrapy.Field()   # 分数
    download = scrapy.Field() # 下载地址
    description = scrapy.Field() # 简介
    pass
