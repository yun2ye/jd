# -*- coding: utf-8 -*-
import scrapy
import copy

class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list_name = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a/text()').extract()
        item = {}
        item['dt_list_name'] = dt_list_name
        for i in range(1, len(dt_list_name)+1):
            dd_list_name = response.xpath('//*[@id="booksort"]/div[2]/dl/dd[{}]/em/a/text()'.format(i)).extract()
            item['dd_list_name'] = dd_list_name
            dd_url = response.xpath('//*[@id="booksort"]/div[2]/dl/dd[{}]/em/a/@href'.format(i)).extract()
            for url in dd_url:
                yield scrapy.Request(
                    url='https:'+url,
                    callback=self.parse_book_list,
                    meta={'item': copy.deepcopy(item)}
                )
                break
            break

    def parse_book_list(self, response):
        item = response.meta.get('item')
        li_list = response.xpath('//*[@id="plist"]/ul/li/div/div[3]/a/em/text()').extract()
        item['li_list'] = li_list
        for i in range(1, len(li_list)+1):
            li_url = 'https:' + response.xpath('//*[@id="plist"]/ul/li[{}]/div/div[1]/a/@href'.format(i)).extract_first()
            yield scrapy.Request(
                url=li_url,
                callback=self.parse_book_detail,
                meta={'item': copy.deepcopy(item)}
            )

    def parse_book_detail(self, response):
        pass