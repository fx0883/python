# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field

class BookItem(Item):
    id = Field()
    title = Field()
    author = Field()
    type = Field()
    description = Field()
    url = Field()
    imageurl = Field()
    readtimes = Field()

class ChapterItem(Item):
    id = Field()
    orderid = Field()
    bookid = Field()
    title = Field()
    url = Field()
    content = Field()

