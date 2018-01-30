# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CarInformation.items import YicheItem, CarInformationLoader


class YicheSpider(CrawlSpider):
    name = 'yiche'
    allowed_domains = ['car.bitauto.com']
    start_urls = ['http://car.bitauto.com/']

    rules = (
        Rule(LinkExtractor(allow=("^http://car.bitauto.com/tree_chexing/.*/$",)), follow=True),
        Rule(LinkExtractor(allow=r'^http://car.bitauto.com/[a-zA-Z0-9-]*/$'), callback='parse_yiche', follow=True),
    )

    def parse_yiche(self, response):
        item_loader = CarInformationLoader(item=YicheItem(), response=response)
        item_loader.add_value('url', response.url)
        car_name = response.css('.crumbs-txt a:nth-last-child(2)::text').extract()[0] + '-' + response.css('.crumbs-txt strong::text').extract()[0]
        item_loader.add_value('car_name', car_name)
        guidance_price = response.css('#cs-area-price::text').extract()
        if not guidance_price:
            guidance_price = '暂无'
        else:
            guidance_price = guidance_price[0]
        item_loader.add_value('guidance_price', guidance_price)
        swept_volume = response.css('.list-justified li:first-child .data::text').extract()
        if not swept_volume:
            swept_volume = '暂无'
        else:
            swept_volume = swept_volume[0]
        item_loader.add_value('swept_volume', swept_volume)
        fuel_economy = response.css('.list-justified li:nth-child(2) .data::text').extract()
        if not fuel_economy:
            fuel_economy = '暂无'
        else:
            fuel_economy = fuel_economy[0].split('>')[0]
        item_loader.add_value('fuel_economy', fuel_economy)
        color = response.css('#color-listbox li a::attr(title)').extract()
        if not color:
            color = '暂无'
        else:
            color = ','.join(x for x in color)
        item_loader.add_value('color', color)
        premium_rate = response.css('.lnk-bzl::text').extract()
        if not premium_rate:
            premium_rate = '暂无'
        else:
            premium_rate = premium_rate[0].split('>')[0]
        item_loader.add_value('premium_rate', premium_rate)
        car_yiche_item = item_loader.load_item()

        yield car_yiche_item
