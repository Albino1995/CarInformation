# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def autohome_get_car_name(value):
    car_name = re.match('<.*>(.*-)<h1>(.*)</h1></a>', value).groups()
    car_name = "".join(x for x in car_name)
    return car_name

def auto_get_structure(list):
    return list[-1]

def auto_get_transmission(list):
    list.pop()
    value =  ','.join(x for x in list)
    return value

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
    color = scrapy.Field(
        output_processor=Join(",")
    )
    engine = scrapy.Field(
        output_processor=Join(",")
    )
    structure = scrapy.Field(
        output_processor=auto_get_structure
    )
    transmission = scrapy.Field(
        output_processor=auto_get_transmission
    )

    def get_insert_sql(self):
        insert_sql = """
                          insert into autohome(url,car_name,guidance_price,color,engine,structure,transmission)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["url"], self["car_name"], self["guidance_price"], self["color"], self["engine"],
                  self["structure"], self["transmission"])

        return insert_sql, params
