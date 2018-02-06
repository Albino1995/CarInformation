# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def autohome_get_car_name(value):
    car_name = re.match('<.*>(.*-)<h1>(.*)</h1></a>', value)
    if not car_name:
        car_name = re.findall('<.*>(.*)</a>', value)
        return car_name[0]
    car_name = "".join(x for x in car_name.groups())
    return car_name



class CarInformationLoader(ItemLoader):
    """
    自定义Itemloader默认取list第一个元素
    """
    default_output_processor = TakeFirst()


class AutohomeItem(scrapy.Item):
    url = scrapy.Field()
    car_name = scrapy.Field(
        input_processor=MapCompose(autohome_get_car_name)
    )
    guidance_price = scrapy.Field()
    color = scrapy.Field()
    engine = scrapy.Field()
    structure = scrapy.Field()
    transmission = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into autohome(url,car_name,guidance_price,color,engine,structure,transmission)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["car_name"], self["guidance_price"], self["color"], self["engine"],
                  self["structure"], self["transmission"])

        return insert_sql, params


class PcautoItem(scrapy.Item):
    url = scrapy.Field()
    car_name = scrapy.Field()
    guidance_price = scrapy.Field()
    swept_volume = scrapy.Field()
    car_type = scrapy.Field()
    transmission = scrapy.Field()
    structure = scrapy.Field()
    color = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into pcauto(url,car_name,guidance_price,swept_volume,car_type,transmission,structure,color)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["car_name"], self["guidance_price"], self["swept_volume"], self["car_type"], self["transmission"],
                  self["structure"], self["color"])

        return insert_sql, params


class YicheItem(scrapy.Item):
    url = scrapy.Field()
    car_name = scrapy.Field()
    guidance_price = scrapy.Field()
    swept_volume = scrapy.Field()
    fuel_economy = scrapy.Field()
    color = scrapy.Field()
    premium_rate = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into yiche(url,car_name,guidance_price,swept_volume,fuel_economy,color,premium_rate)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["car_name"], self["guidance_price"], self["swept_volume"], self["fuel_economy"], self["color"],
                  self["premium_rate"])

        return insert_sql, params


class AutoSinaItem(scrapy.Item):
    url = scrapy.Field()
    car_name = scrapy.Field()
    guidance_price = scrapy.Field()
    engine = scrapy.Field()
    transmission = scrapy.Field()
    car_type = scrapy.Field()
    color = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into autosina(url,car_name,guidance_price,engine,transmission,car_type,color)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["car_name"], self["guidance_price"], self["engine"], self["transmission"], self["car_type"],
                  self["color"])

        return insert_sql, params


class YicheForumItem(scrapy.Item):
    url = scrapy.Field()
    forum_name = scrapy.Field()
    theme_num = scrapy.Field()
    posts_num = scrapy.Field()
    essence_posts_num = scrapy.Field()
    owner_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into yiche_forum(url,forum_name,theme_num,posts_num,essence_posts_num,owner_num,crawl_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["forum_name"], self["theme_num"], self["posts_num"], self["essence_posts_num"], self["owner_num"],
                  self["crawl_time"])

        return insert_sql, params