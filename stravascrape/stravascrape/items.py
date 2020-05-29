# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RideItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ride_id = scrapy.Field() #response is 'id'
    name = scrapy.Field()
    activity_type_display_name = scrapy.Field()
    bike_id = scrapy.Field()
    calories = scrapy.Field()
    distance = scrapy.Field()
    distance_raw = scrapy.Field()
    elapsed_time = scrapy.Field()
    elapsed_time_raw = scrapy.Field()
    elevation_gain = scrapy.Field()
    elevation_gain_raw = scrapy.Field()
    elevation_unit = scrapy.Field()
    long_unit = scrapy.Field()
    moving_time = scrapy.Field()
    moving_time_raw = scrapy.Field()
    short_unit = scrapy.Field()
    start_date = scrapy.Field()
    start_date_local_raw = scrapy.Field()
    start_day = scrapy.Field()
    start_time = scrapy.Field()
    ride_type = scrapy.Field() #response is 'type'
    visibility = scrapy.Field()

class RidePageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ride_id = scrapy.Field() #response is 'id'
    avg_watts = scrapy.Field()
    max_watts = scrapy.Field()
    watts_type = scrapy.Field()
    distance = scrapy.Field()
    time = scrapy.Field()
    elevation = scrapy.Field()
    kJ = scrapy.Field()
    avg_speed = scrapy.Field()
    max_speed = scrapy.Field()
    avg_cad = scrapy.Field()
    max_cad = scrapy.Field()
    Calories = scrapy.Field()
    avg_temp = scrapy.Field()
   	


    
