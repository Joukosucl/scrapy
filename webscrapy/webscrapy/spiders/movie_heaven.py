# coding:utf8

import scrapy
from webscrapy.items import movieItem
from scrapy.http import Request

import re

class MvHeavenSpider(scrapy.Spider):
    name = "mvheaven"

    start_urls = [
        "http://www.dytt8.net/html/gndy/rihan/index.html", # japan, korea
        #"http://www.ygdy8.net/html/gndy/dyzz/index.html", # new
        #"http://www.ygdy8.net/html/gndy/china/index.html", # inner
        #"http://www.ygdy8.net/html/gndy/oumei/index.html"  # europe
    ] 

    url_head = 'http://www.dytt8.net/'

    # init item object
    item = movieItem()
    item['zh_name'] = ''
    item['en_name'] = ''
    item['movie_time'] = ''
    item['language'] = ''
    item['file_type'] = ''
    item['movie_type'] = ''
    item['resolution'] = ''
    item['movie_length'] = ''
    item['director'] = ''
    item['main_actor'] = ''
    item['add_time'] = ''
    item['subtitle'] = ''
    item['country'] = ''
    item['score'] = ''
    item['download'] = ''
    item['description'] = ''

    def value_assign(self, item, key, value):
        
        if key == u'译名':      item['zh_name'] = value
        elif key == u'片名': item['en_name'] = value 
        elif key == u'年代': item['movie_time'] = value
        elif key in (u'国家',u'地区'): item['country'] = value    
        elif key == u'类别': item['movie_type'] = value.replace(u'/',u',')
        elif key == u'语言': item['language'] = value
        elif key == u'字幕': item['subtitle'] = value
        elif key == u'IMDb评分': item['score'] = value
        elif key == u'文件格式': item['file_type'] = value
        elif key == u'视频尺寸': item['resolution'] = value.replace(u' ',u'')
        elif key == u'片长':  item['movie_length'] = value.replace(u'分钟',u'')
        elif key == u'导演':  item['director'] = value.split(u' ', 1)[0]
        elif key == u'主演':  
            item['main_actor'] = ','.join([people.split(u' ', 1)[0] for people in value.split(u',')])
        elif key == u'简介':     item['description'] = value.strip()
        elif key == u'下载地址': item['download'] = value.strip()

    def parse_detail(self, response):
        '''
        parse detail movie info and send into items
        '''

        infos = response.xpath('//div[@id="Zoom"]//text()').extract()

        key, value = '', ''
        
        for info in infos:
            clear_info = info.strip().replace(u'　　',u'')

            # continue if info is blank
            if not clear_info:
                continue

            # assign the last value into item instance
            self.value_assign(self.item, key, value)

            if u'◎' in clear_info:
                result = re.split(u'　| ', clear_info.replace(u'◎' ,u''), maxsplit=1)
                if len(result) > 1:
                    key, value = result
                else:
                    key = result[0]
            else:
                if key == u'主演':
                    value += u','+clear_info
                elif u'下载' in clear_info:
                    key = u'下载地址'
                    value = ''
                else:
                    value = clear_info
       
        # assign download url to item
        self.value_assign(self.item, key, value)

        yield self.item
           
                

    def parse(self, response):
        '''
        parse the page
        '''

        # determin the url of the next page
        next_page = response.xpath('//a[text()="%s"]/@href' % u'下一页').extract()
        pos = response.url.rfind(u'/',1)
        next_url = response.url[:pos+1] + next_page[0]

        # parse the list
        movies = response.xpath('//table[@class="tbspan"]')
        
        for source in movies:
            link = source.xpath('.//a[@class="ulink"][last()]/@href').extract()[0]
            add_time = source.xpath('.//font/text()').extract()[0]
            add_time = add_time.split(u'：')[1].split(u'\n')[0]
           
            #print self.url_head + link
            yield scrapy.Request(self.url_head + link, callback = self.parse_detail)

        if next_page:
            yield scrapy.Request(next_url, callback = self.parse)
                
