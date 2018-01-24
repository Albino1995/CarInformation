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
