import scrapy
from futgalCrawler.items import GoalscorerItem
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class GoalscorersSpider(scrapy.Spider):
    name = "goalscorers_spider"
    allowed_domains = ["www.futgal.es"]

    # Start URL
    start_urls = ["https://www.futgal.es/pnfg/NPcd/NFG_Mov_LstCompeticiones?cod_primaria=&competicion=1&goles=1"]

    def parse(self, response):

        # Lista de categorías permitidas
        categorias = [
            "https://www.futgal.es/pnfg/NPcd/NFG_Mov_LstGruposCompeticion?cod_primaria=&buscar=1&codcompeticion=20005937&goles=1",
            "https://www.futgal.es/pnfg/NPcd/NFG_Mov_LstGruposCompeticion?cod_primaria=&buscar=1&codcompeticion=20005965&goles=1",
        ]

        # Construir expresión XPath que coincida con cualquiera de las categorías permitidas
        textos_xpath = " or ".join([f'contains(.//strong, "{texto}")' for texto in categorias])

        # Extraer los enlaces a cada grupo
        grupo_links = response.xpath(f'//a[contains(@href, "NFG_Mov_LstGruposCompeticion") and ({textos_xpath})]/@href').getall()

        formatted_links = "\n".join(grupo_links)
        total_links = len(grupo_links)
    
        self.logger.info(f"Enlaces extraídos:\n{formatted_links}\n\nTotal de enlaces: {total_links}\n")

        for link in categorias:
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_grupo_links)
            

    def parse_grupo_links(self, response): 
        self.logger.info(f"Procesando datos del grupo: {response.url}")     
        # Extraer los enlaces a cada grupo
        grupo_links_internos = response.xpath('//a[contains(@href, "NFG_CMP_Goleadores")]/@href').getall()

        formatted_links_intern = "\n".join(grupo_links_internos)
        total_links_intern = len(grupo_links_internos)
        
        self.logger.info(f"Enlaces extraídos internos:\n{formatted_links_intern}\n\nTotal de enlaces internos: {total_links_intern}\n")

        for link_interno in grupo_links_internos:
            # Analiza el enlace
            parsed_url = urlparse(link_interno)
            query_params = parse_qs(parsed_url.query)

            # Reconstruye el enlace con los nuevos parámetros
            new_query = urlencode(query_params, doseq=True)
            new_link = urlunparse(parsed_url._replace(query=new_query))

            full_link = response.urljoin(new_link)  # Convierte el enlace relativo en absoluto
            yield scrapy.Request(full_link, callback=self.parse_competition)

    def parse_competition(self, response):

        goalscorers = response.xpath('//table//tr')

        for index, goalscorer in enumerate(goalscorers):
            rows =  response.xpath('//tbody/tr')

            crawled_goalscorer = GoalscorerItem()
            crawled_goalscorer['name'] = goalscorer.xpath('.//td[1]/text()').get()
            crawled_goalscorer['team'] = goalscorer.xpath('.//td[2]/text()').get()
            crawled_goalscorer['category'] = goalscorer.xpath('//div[@class="col-sm-12" and @style="text-align:center;"]/h4/text()').get().strip()
            crawled_goalscorer['group'] = goalscorer.xpath('.//td[3]/text()').get()
            games_played = goalscorer.xpath('.//td[4]/text()').get()
            if games_played:
                crawled_goalscorer['games_played'] = games_played.strip()
            else:
                crawled_goalscorer['games_played'] = None
            crawled_goalscorer['goals'] = goalscorer.xpath('.//td[5]/strong/text()').get()
            crawled_goalscorer['goal_ratio'] = goalscorer.xpath('.//td[6]/text()').get()

            if crawled_goalscorer['name'] and crawled_goalscorer['team'] and crawled_goalscorer['games_played'] and crawled_goalscorer['goals'] and crawled_goalscorer['goal_ratio']:
                yield crawled_goalscorer
