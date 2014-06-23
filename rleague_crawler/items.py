# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RleagueCrawlerItem(Item):
    teamone     = Field()
    teamtwo     = Field()
    scrums      = Field()
    penalties   = Field()
    referees    = Field()
    venue       = Field()
    crowd       = Field()
    date        = Field()
    link        = Field()

