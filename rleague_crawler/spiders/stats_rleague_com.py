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
            'name':    ''.join(sel.xpath('normalize-space(//table//tr[1]/th[1])').extract()),
            'players': [],
        }

        i['teamtwo'] = {
            'name':    ''.join(sel.xpath('normalize-space(//table//tr[1]/th[2])').extract()),
            'players': [],
        }
        
        for tr in sel.xpath('//table//tr[position() > 2 and position() < last() - 1]'): 
            i['teamone']['players'].append({
                'pos':      ''.join(tr.xpath('td[1]//text()').extract()).strip(),
                'player':   ''.join(tr.xpath('td[2]//text()').extract()).strip(),
                't':        ''.join(tr.xpath('td[3]//text()').extract()).strip(),
                'g':        ''.join(tr.xpath('td[4]//text()').extract()).strip(),
                'fg':       ''.join(tr.xpath('td[5]//text()').extract()).strip(),
                'pts':      ''.join(tr.xpath('td[6]//text()').extract()).strip(),
            })

            i['teamtwo']['players'].append({
                'pos':      ''.join(tr.xpath('td[7]//text()').extract()).strip(),
                'player':   ''.join(tr.xpath('td[8]//text()').extract()).strip(),
                't':        ''.join(tr.xpath('td[9]//text()').extract()).strip(),
                'g':        ''.join(tr.xpath('td[10]//text()').extract()).strip(),
                'fg':       ''.join(tr.xpath('td[11]//text()').extract()).strip(),
                'pts':      ''.join(tr.xpath('td[12]//text()').extract()).strip(),
            })


        i['scrums']     = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Scrums")]/following-sibling::text()[1])').extract())
        i['penalties']  = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Penalties")]/following-sibling::text()[1])').extract())
        i['referees']   = sel.xpath('//table//tr[last()]/td/*[contains(., "Venue")]/preceding-sibling::a//text()').extract()
        i['venue']      = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Venue")]/following-sibling::*[1]/text())').extract())
        i['crowd']      = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Crowd")]/following-sibling::text()[1])').extract())
        i['date']       = ''.join(sel.xpath('normalize-space(//table//tr[last()]/td/*[contains(., "Date")]/following-sibling::text()[1])').extract())
        i['link']       = response.url

        if i['teamone'] != '':
            return i
