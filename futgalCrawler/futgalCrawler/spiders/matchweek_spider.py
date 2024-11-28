import scrapy
from futgalCrawler.items import FutgalcrawlerItem, MatchItem
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class FutgalSpiderSpider(scrapy.Spider):
    name = "matchweek_spider"
    allowed_domains = ["www.futgal.es"]
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_Mov_LstGruposCompeticion?cod_primaria=&buscar=1&codcompeticion=20005937&rt=1"]

    def parse(self, response):
        # Extraer los enlaces a cada grupo
        grupo_links = response.xpath('//a[contains(@href, "NFG_CmpJornada")]/@href').getall()

        self.logger.info(f"Enlaces extraídos: {len(grupo_links)} grupos encontrados.")

        for link in grupo_links:
            # Analiza el enlace
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)

            # Establece CodJornada=1
            query_params['CodJornada'] = ['34']

            # Reconstruye el enlace con los nuevos parámetros
            new_query = urlencode(query_params, doseq=True)
            new_link = urlunparse(parsed_url._replace(query=new_query))

            full_link = response.urljoin(new_link)  # Convierte el enlace relativo en absoluto
            yield scrapy.Request(full_link, callback=self.parse_partidos)

    def parse_partidos(self, response):
        partidos = response.xpath('//table')

        all_h3_texts = response.xpath('//div[contains(@class, "col-sm-12")]/h3//text()').getall()
        all_h3_texts = [text.strip() for text in all_h3_texts if text.strip()]

        season = " ".join(all_h3_texts[0].split()[1:]).strip()
        match_week = all_h3_texts[3]
        category_and_group = all_h3_texts[1]
        category = " ".join(category_and_group.split()[:2]).strip()
        group = " ".join(category_and_group.split()[2:]).strip()
        
        for index, partido in enumerate(partidos):
            if index == 0:  # Salta la cabecera si hay una
                continue

            match = MatchItem()
            match['home_team'] = partido.xpath('.//td[1]//a/text()').get().strip() if partido.xpath('.//td[1]//a/text()').get() else None
            match['away_team'] = partido.xpath('.//td[3]//a/text()').get().strip() if partido.xpath('.//td[3]//a/text()').get() else None
            match['date'] = partido.xpath('.//span[contains(@class, "horario")][1]/text()').get().strip() if partido.xpath('.//span[contains(@class, "horario")][1]/text()').get() else None
            match['time'] = partido.xpath('.//span[contains(@class, "horario")][2]/text()').get().strip() if partido.xpath('.//span[contains(@class, "horario")][2]/text()').get() else None
            match['field'] = partido.xpath('.//tr[2]/td[contains(@colspan, "9")]//a/text()').get().strip() if partido.xpath('.//tr[2]/td[contains(@colspan, "9")]//a/text()').get() else None
            match['season'] = season
            match['category'] = category
            match['group'] = group
            match['match_week'] = match_week
            
            raw_referee = partido.xpath('.//tr[2]/td[contains(@colspan, "9")]//span[@class= "font_widgetL"]/text()').getall()
            clean_referee = [a.strip() for a in raw_referee if a.strip()]

            match['referee'] = clean_referee[-1] if len(clean_referee) == 2 else None

            yield match
