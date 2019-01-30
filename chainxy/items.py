# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ChainItem(Item):

    Product_Name = Field()

    Weight = Field()

    Unit = Field()

    Number_Per_Unit = Field()

    Storage_Form = Field()

    Number_Whole_Package = Field()

    Art_Nr_Supplier = Field()

    Article_Number = Field()

    Country = Field()

    GTIN = Field()

    Category = Field()