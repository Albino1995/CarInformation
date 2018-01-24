# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CarInformation.items import AutohomeItem, CarInformationLoader


class AutohomeSpider(CrawlSpider):
    name = 'autohome'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/car/']

    rules = (
        Rule(LinkExtractor(allow=("^https://www.autohome.com.cn/a00/$",)), follow=True),
        Rule(LinkExtractor(allow=("^https://www.autohome.com.cn/a0/$",)), follow=True),
        Rule(LinkExtractor(allow=("^https://www.autohome.com.cn/[a-z]{1,3}/$",)), follow=True),
        Rule(LinkExtractor(allow=r'^https://www.autohome.com.cn/\d+/#.*'), callback='parse_car_autohome', follow=True),
    )

    def parse_car_autohome(self, response):
        item_loader = CarInformationLoader(item=AutohomeItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_css('car_name', '.subnav-title-name a')
        guidance_price = response.xpath('//*[@class="autoseries-info"]/dl/dt[1]/a[1]/text()')
        if not guidance_price:
            guidance_price = '暂无'
        else:
            guidance_price = guidance_price.extract()[0]
        item_loader.add_value('guidance_price', guidance_price)
        color = response.css('.car-color-con a .tip .tip-content::text')
        if not color:
            color = '暂无'
        else:
            color = ",".join(x for x in color.extract())
        item_loader.add_value('color', color)
        engine = response.css('.car-color+dd a::text')
        if not engine:
            engine = '暂无'
        else:
            engine = engine.extract()[0]
        item_loader.add_value('engine', engine)
        structure_transmission = response.css('.car-color+dd+dd a::text')
        if not structure_transmission:
            structure = '暂无'
            transmission = '暂无'
        else:
            structure = structure_transmission.extract()[-1]
            structure_transmission.extract().pop()
            transmission = ",".join(x for x in structure_transmission.extract())
        item_loader.add_value('structure', structure)
        item_loader.add_value('transmission', transmission)

        car_autohome_item = item_loader.load_item()

        yield car_autohome_item



