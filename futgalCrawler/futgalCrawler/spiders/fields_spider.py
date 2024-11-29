import scrapy
from futgalCrawler.items import FieldItem
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class FieldsSpider(scrapy.Spider):
    name = "fields_spider"
    allowed_domains = ["www.futgal.es"]

    # Start URL
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_LstCampos?cod_primaria=1000122&NPcd_PageLines=0"]

    # Parse method to extract fields
    def parse(self, response):
        fields = response.xpath('//table//tr')

        for index, field in enumerate(fields):
            rows =  response.xpath('//table//tr')

            crawled_field = FieldItem()
            crawled_field['name'] = field.xpath('.//td[1]/a/text()').get().strip() if field.xpath('.//td[1]/a/text()').get() else None
            crawled_field['direction'] = field.xpath('.//td[2]/text()').get().strip() if field.xpath('.//td[2]/text()').get() else None
            crawled_field['city'] = field.xpath('.//td[3]/text()').get().strip() if field.xpath('.//td[3]/text()').get() else None
            crawled_field['type'] = field.xpath('.//td[5]/text()').get().strip() if field.xpath('.//td[5]/text()').get() else None

            if crawled_field['name']:
                yield crawled_field
