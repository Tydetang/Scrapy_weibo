# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class WeiboItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'weibo'
    id = Field()
    content = Field()
    forward_count = Field()
    comment_count = Field()
    like_count = Field()
    posted_at = Field()
    url = Field()
    user = Field()
    crawled_at = Field()

class Weibo_userItem(Item):
    table_name = 'weibouser'
    user_id = Field()
    # user_province = Field()
    user_city = Field()
    user_sex = Field()
    user_age = Field()
    user_fans = Field()
    user_birthday = Field()