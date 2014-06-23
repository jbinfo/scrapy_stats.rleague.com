from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from rleague_crawler.items import RleagueCrawlerItem

class StatsRleagueComSpider(CrawlSpider):
    name = 'stats_rleague_com'
    allowed_domains = ['stats.rleague.com']
    start_urls = ['http://stats.rleague.com/rl/seas/2014.html']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'scorers/games/2014/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = RleagueCrawlerItem()

        i['teamone'] = {
            'name':     ''.join(sel.xpath('normalize-space(//table//tr[1]/th[1])').extract()),
            'pos':      '',
            'player':   '',
            't':        '',
            'g':        '',
            'fg':       '',
            'pts':      '',
        }

        i['teamtwo'] = {
            'name':     ''.join(sel.xpath('normalize-space(//table//tr[1]/th[2])').extract()),
            'pos':      '',
            'player':   '',
            't':        '',
            'g':        '',
            'fg':       '',
            'pts':      '',
        }
        
        for tr in sel.xpath('//table//tr[position() > 2 and position() < last() - 1]'):
            i['teamone']['pos']     = ''.join(tr.xpath('normalize-space(td[1]//text())').extract())
            i['teamone']['player']  = ''.join(tr.xpath('normalize-space(td[2]//text())').extract())
            i['teamone']['t']       = ''.join(tr.xpath('normalize-space(td[3]//text())').extract())
            i['teamone']['g']       = ''.join(tr.xpath('normalize-space(td[4]//text())').extract())
            i['teamone']['fg']      = ''.join(tr.xpath('normalize-space(td[5]//text())').extract())
            i['teamone']['pts']     = ''.join(tr.xpath('normalize-space(td[6]//text())').extract())

            i['teamtwo']['pos']     = ''.join(tr.xpath('normalize-space(td[7]//text())').extract())
            i['teamtwo']['player']  = ''.join(tr.xpath('normalize-space(td[8]//text())').extract())
            i['teamtwo']['t']       = ''.join(tr.xpath('normalize-space(td[9]//text())').extract())
            i['teamtwo']['g']       = ''.join(tr.xpath('normalize-space(td[10]//text())').extract())
            i['teamtwo']['fg']      = ''.join(tr.xpath('normalize-space(td[11]//text())').extract())
            i['teamtwo']['pts']     = ''.join(tr.xpath('normalize-space(td[12]//text())').extract())


        i['scrums']     = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Scrums")]/following-sibling::text()[1])').extract())
        i['penalties']  = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Penalties")]/following-sibling::text()[1])').extract())
        i['referees']   = sel.xpath('//table//tr[last()]/td/*[contains(., "Venue")]/preceding-sibling::a//text()').extract()
        i['venue']      = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Venue")]/following-sibling::*[1]/text())').extract())
        i['crowd']      = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Crowd")]/following-sibling::text()[1])').extract())
        i['date']       = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Date")]/following-sibling::text()[1])').extract())
        i['link']       = response.url

        if i['teamone'] != '':
            return i
