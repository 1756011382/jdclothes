# -*- coding: utf-8 -*-
import scrapy
from clothes.items import ClothesItem
import re
import json

class JdclothesSpider(scrapy.Spider):
    name = 'jdclothes'
    # allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']
    url = 'https://search.jd.com/Search?keyword=%E8%A1%A3%E6%9C%8D&enc=utf-8&wq=%E8%A1%A3%E6%9C%8D&pvid=067d20f315a94c569f89303b4fa430cc'

    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse_product)

    def parse_product(self, response):
        productid = response.css('li.gl-item::attr(data-sku)').extract()
        productid = list(set(productid))
        for product in productid:
            url_comment = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv11&productId='+product+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url_comment,callback=self.parse_page)

    def parse_page(self, response):
        productid = re.search(r'productId=(\d+)&',response.url).group(1)
        maxpage = int(re.search(r'"maxPage":(\d+),',response.text).group(1))
        for page in range(maxpage):
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4503&productId='+productid+'&score=0&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_comment)

    def parse_comment(self, response):
        html = response.text.replace('fetchJSON_comment98vv4503(','')
        html = html.replace(');','')
        comment = json.loads(html)
        results = comment['comments']
        for i in range(len(results)):
            item  = ClothesItem()
            item['content'] =results[i]['content']
            item['creationTime']=results[i]['creationTime']
            item['id'] = results[i]['id']
            item['productColor'] = results[i]['productColor']
            item['productSize'] = results[i]['productSize']
            item['score'] = results[i]['score']
            item['userClientShow'] = results[i]['userClientShow']
            item['userLevelName'] = results[i]['userLevelName']
            yield item