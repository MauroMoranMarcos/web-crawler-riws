import scrapy
from  futgalCrawler.items import FutgalcrawlerItem


class FutgalSpiderSpider(scrapy.Spider):
    name = "futgal_spider"
    allowed_domains = ["www.futgal.es"]
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120&CodActa=1193585&cod_acta=1193585"]

    def parse(self, response):
        item = FutgalcrawlerItem()
        item['team'] = response.css('div.page-wrapper div.page-wrapper-row full-height div.page-wrapper-middle div.page-container div.page-content-wrapper div.page-content div.container div.row nova_text div.dashboard-stat grey div.details div.desc table.table table-stripped table-hover tr::text').get()

        yield item

#    def parse(self, response):
 #       for futgal in response.css('div.page-wrapper div.page-wrapper-row full-height div.page-wrapper-middle div.page-container div.page-content-wrapper div.page-content div.container div.row nova_text div.dashboard-stat grey div.details div.desc table.table table-stripped table-hover'):
  #          item = FutgalcrawlerItem()
   #         item['team'] = futgal.css('tr::text').get()

    #        yield item
