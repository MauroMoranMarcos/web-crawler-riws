import scrapy


class OlaSpider(scrapy.Spider):
    name = "ola"
    allowed_domains = ["www.futgal.es"]
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120"]

    def parse(self, response):
        pass
