# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CarInformation.items import PcautoItem, CarInformationLoader


class PcatutoSpider(CrawlSpider):
    name = 'pcatuto'
    allowed_domains = ['price.pcauto.com.cn']
    start_urls = ['http://price.pcauto.com.cn/cars/']

    rules = (
        Rule(LinkExtractor(allow=r'^http://price.pcauto.com.cn/sg\d+/$'), callback='parse_car_pcauto', follow=True),
    )

    def parse_car_pcauto(self, response):
        item_loader = CarInformationLoader(item=PcautoItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_css('car_name', '.title h1::text')
        guidance_price = response.css('#dfCtrId::text').extract()
        if not guidance_price:
            guidance_price = '停售'
        else:
            guidance_price = guidance_price[0]
        item_loader.add_value('guidance_price', guidance_price)
        swept_volume = response.css('.BG+.des li:first-child p em a::text').extract()
        if not swept_volume:
            swept_volume = '暂无'
        else:
            swept_volume = ','.join(x for x in swept_volume)
        item_loader.add_value('swept_volume', swept_volume)
        car_type = response.css('.BG+.des li:first-child p:last-child a::text').extract()
        if not car_type:
            car_type = '暂无'
        else:
            car_type = ','.join(x for x in car_type)
        item_loader.add_value('car_type', car_type)
        transmission = response.css('.BG+.des li:last-child p:first-child em a::text').extract()
        if not transmission:
            transmission = '暂无'
        else:
            transmission = ','.join(x for x in transmission)
        item_loader.add_value('transmission', transmission)
        structure = response.css('.BG+.des li:last-child p:last-child em a::text').extract()
        if not structure:
            structure = '暂无'
        else:
            structure = ','.join(x for x in structure)
        item_loader.add_value('structure', structure)
        color = response.css('.cInner a .tip::text').extract()
        if not color:
            color = '暂无'
        else:
            color = ','.join(x for x in color)
        item_loader.add_value('color', color)
        car_autohome_item = item_loader.load_item()
        yield car_autohome_item