# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CarInformation.items import AutoSinaItem, CarInformationLoader


class AutosinaSpider(CrawlSpider):
    name = 'autosina'
    allowed_domains = ['db.auto.sina.com.cn']
    start_urls = ['http://db.auto.sina.com.cn/']

    rules = (
        Rule(LinkExtractor(allow=("^http://db.auto.sina.com.cn/b\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'^http://db.auto.sina.com.cn/\d+/$'), callback='parse_auto_sina', follow=True),
    )

    def parse_auto_sina(self, response):
        item_loader = CarInformationLoader(item=AutoSinaItem(), response=response)
        item_loader.add_value('url', response.url)

        car_name = response.css('.fL+.name a::text').extract()
        car_name = '-'.join(x for x in car_name)
        item_loader.add_value('car_name', car_name)

        guidance_price = response.css('.info li:first-child span::text').extract()
        if not guidance_price:
            guidance_price = '暂无'
        else:
            guidance_price = guidance_price[0]
        item_loader.add_value('guidance_price', guidance_price)

        engine = response.css('.info li:nth-child(3) span::text').extract()
        if not engine:
            engine = '暂无'
        else:
            engine = engine[0]
        item_loader.add_value('engine', engine)

        transmission = response.css('.info li:nth-child(4) span::text').extract()
        if not transmission:
            transmission = '暂无'
        else:
            transmission = transmission[0]
        item_loader.add_value('transmission', transmission)

        car_type = response.css('.info li:last-child span::text').extract()
        if not car_type:
            car_type = '暂无'
        else:
            car_type = car_type[0]
        item_loader.add_value('car_type', car_type)

        color = response.css('#rec_colorb1 ul li .color span::text').extract()
        if not color:
            color = '暂无'
        else:
            color = ','.join(x for x in color)
        item_loader.add_value('color', color)


        auto_sina_item = item_loader.load_item()

        yield auto_sina_item
