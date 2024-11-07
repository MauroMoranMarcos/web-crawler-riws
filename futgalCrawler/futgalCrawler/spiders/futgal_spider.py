import scrapy
from  futgalCrawler.items import FutgalcrawlerItem, MatchItem
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


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
    #allowed_domains = ["www.fexfutbol.com"]
    allowed_domains = ["www.futgal.es"]
    #start_urls = ["https://www.fexfutbol.com/pnfg/NPcd/NFG_Mov_LstGruposCompeticion?cod_primaria=&buscar=1&codcompeticion=6346931&rt=1"]
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_Mov_LstGruposCompeticion?cod_primaria=&buscar=1&codcompeticion=20005937&rt=1"]
    #start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120&CodCompeticion=20005937&CodGrupo=22011727&CodTemporada=20&CodJornada=4&Sch_Codigo_Delegacion=3&Sch_Tipo_Juego="]

    def parse(self, response):
        # Extraer los enlaces a cada grupo
        grupo_links = response.xpath('//a[contains(@href, "NFG_CmpJornada")]/@href').getall()

        formatted_links = "\n".join(grupo_links)  # Une los enlaces con salto de línea
        total_links = len(grupo_links)  # Cuenta el total de enlaces
    
        # Registra la información
        self.logger.info(f"Enlaces extraídos:\n{formatted_links}\n\nTotal de enlaces: {total_links}\n")

        for link in grupo_links:
            # Analiza el enlace
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)

            # Establece CodJornada=1
            query_params['CodJornada'] = ['1']

            # Reconstruye el enlace con los nuevos parámetros
            new_query = urlencode(query_params, doseq=True)
            new_link = urlunparse(parsed_url._replace(query=new_query))

            full_link = response.urljoin(new_link)  # Convierte el enlace relativo en absoluto
            yield scrapy.Request(full_link, callback=self.parse_partidos)

    def parse_partidos(self, response):
        partidos = response.xpath('//table')

        current_url = response.url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)
        current_jornada = int(query_params.get('CodJornada', [1])[0])  # Obtén el valor actual, por defecto 1

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

        # Buscar el enlace de la siguiente jornada
        next_matchday = response.xpath('//a[contains(@class, "btn green-meadow")]/@href').get()

        if next_matchday:
            # Aquí necesitas extraer los parámetros necesarios para construir la URL correcta
            cod_competicion = query_params.get('CodCompeticion', [''])[0]  # Extrae CodCompeticion
            grupo = query_params.get('CodGrupo', [''])[0]  # Extrae CodGrupo
            cod_temporada = "20"  # Ajusta esto según sea necesario

            # Incrementa CodJornada
            next_jornada = current_jornada + 1

            # Construye la nueva URL para la siguiente jornada
            next_jornada_url = f"/pnfg/NPcd/NFG_CmpJornada?cod_primaria=1000120&CodCompeticion={cod_competicion}&CodGrupo={grupo}&CodTemporada={cod_temporada}&CodJornada={next_jornada}"

            yield scrapy.Request(response.urljoin(next_jornada_url), callback=self.parse_partidos)


#    def parse(self, response):
 #       for futgal in response.css('div.page-wrapper div.page-wrapper-row full-height div.page-wrapper-middle div.page-container div.page-content-wrapper div.page-content div.container div.row nova_text div.dashboard-stat grey div.details div.desc table.table table-stripped table-hover'):
  #          item = FutgalcrawlerItem()
   #         item['team'] = futgal.css('tr::text').get()

    #        yield item
