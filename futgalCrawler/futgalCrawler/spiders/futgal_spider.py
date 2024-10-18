import scrapy
from  futgalCrawler.items import FutgalcrawlerItem, MatchItem


#class FutgalSpiderSpider(scrapy.Spider):
    #name = "futgal_spider"
    #allowed_domains = ["www.futgal.es"]
    #start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120&CodActa=1193585&cod_acta=1193585"]

    #def parse(self, response):
        #item = FutgalcrawlerItem()
        #item['team'] = response.css('div.font_widgetL::text').get()
        
        #yield item

class FutgalSpiderSpider(scrapy.Spider):
    name = "futgal_spider"
    allowed_domains = ["www.futgal.es"]
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120&CodCompeticion=20005937&CodGrupo=22011727&CodTemporada=20&CodJornada=6&Sch_Codigo_Delegacion=3&codigo_tipo_juego=1"]
    #start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120&CodCompeticion=20005937&CodGrupo=22011727&CodTemporada=20&CodJornada=4&Sch_Codigo_Delegacion=3&Sch_Tipo_Juego="]
    
    def parse(self, response):
        partidos = response.xpath('//table')

        for index, partido in enumerate(partidos):

            if index == 0:
                continue

            match = MatchItem()
            match['home_team'] = partido.xpath('.//td[1]//a/text()').get()
            match['away_team'] = partido.xpath('.//td[3]//a/text()').get()
            match['date'] = partido.xpath('.//span[contains(@class, "horario")][1]/text()').get()
            match['time'] = partido.xpath('.//span[contains(@class, "horario")][2]/text()').get()
            match['field'] = partido.xpath('.//tr[2]/td[contains(@colspan, "9")]//a/text()').get()
            
            raw_referee = partido.xpath('.//tr[2]/td[contains(@colspan, "9")]//span[@class= "font_widgetL"]/text()').getall()
            clean_referee = [a.strip() for a in raw_referee if a.strip()]

            match['referee'] = clean_referee[-1] if clean_referee else None

            yield match


#    def parse(self, response):
 #       for futgal in response.css('div.page-wrapper div.page-wrapper-row full-height div.page-wrapper-middle div.page-container div.page-content-wrapper div.page-content div.container div.row nova_text div.dashboard-stat grey div.details div.desc table.table table-stripped table-hover'):
  #          item = FutgalcrawlerItem()
   #         item['team'] = futgal.css('tr::text').get()

    #        yield item
