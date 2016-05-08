# -*- coding: utf-8 -*-
import scrapy
from dmoz.items import DmozItem

class DmozSpiderSpider(scrapy.Spider):
    name = "dmoz_spider"
    allowed_domains = ["dmoz.org"]
    start_urls = (
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
    )

    def parse(self, response):
        # filename = response.url.split('/')[-2] + '.html'
        # with open(filename, 'wb') as f:
        #    f.write(response.body)
        lis = response.xpath('/html/body/div[2]/div[3]/fieldset[3]/ul/li[1]')
        for li in lis:
            item = DmozItem()
            item['title'] = li.xpath('a/text()').extract()
            item['link'] = li.xpath('a/@href').extract()
            item['desc'] = li.xpath('text()')
            yield item
