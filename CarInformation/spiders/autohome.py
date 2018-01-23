# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CarInformation.items import AutohomeItem, CarInformationLoader


class AutohomeSpider(CrawlSpider):
    name = 'autohome'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://www.autohome.com.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'^https://www.autohome.com.cn/\d+/#pvareaid=\d+'), callback='parse_car_autohome', follow=False),
    )

    def parse_car_autohome(self, response):
        item_loader = CarInformationLoader(item=AutohomeItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_css('car_name', '.subnav-title-name a')
        item_loader.add_xpath('guidance_price', '//*[@class="autoseries-info"]/dl/dt[1]/a[1]/text()')
        item_loader.add_css('color', '.car-color-con a .tip .tip-content::text')
        item_loader.add_css('engine', '.car-color+dd a::text')
        item_loader.add_css('structure', '.car-color+dd+dd a::text')
        item_loader.add_css('transmission', '.car-color+dd+dd a::text')

        car_autohome_item = item_loader.load_item()

        yield car_autohome_item



