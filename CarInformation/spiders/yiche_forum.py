# -*- coding: utf-8 -*-
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

from CarInformation.items import YicheForumItem, CarInformationLoader


class YicheForumSpider(CrawlSpider):
    name = 'yiche_forum'
    allowed_domains = ['baa.bitauto.com']
    start_urls = ['http://baa.bitauto.com/foruminterrelated/brandforumlist.html']

    rules = (
        Rule(LinkExtractor(allow=("^http://baa.bitauto.com/foruminterrelated/brandforumlist_by_tree.html.*$",)), follow=True),
        Rule(LinkExtractor(allow=r'^http://baa.bitauto.com/\w+$'), callback='parse_yiche_forum', follow=True),
        Rule(LinkExtractor(allow=r'^http://baa.bitauto.com/\w+/$'), callback='parse_yiche_forum', follow=True),
    )

    def parse_yiche_forum(self, response):
        item_loader = CarInformationLoader(item=YicheForumItem(), response=response)
        item_loader.add_value('url', response.url)
        forum_name = response.css('.name_photo h1::text').extract()[0].strip()
        item_loader.add_value('forum_name', forum_name)
        item_loader.add_css('theme_num', '.list_box ul li:first-child em::text')
        item_loader.add_css('posts_num', '.list_box ul li:nth-child(2) em::text')
        item_loader.add_css('essence_posts_num', '.list_box ul li:nth-last-child(2) em::text')
        item_loader.add_css('owner_num', '.list_box ul li:last-child em::text')
        item_loader.add_value('crawl_time', datetime.datetime.now())
        yiche_forum_item = item_loader.load_item()
        time.sleep(3)
        yield yiche_forum_item
