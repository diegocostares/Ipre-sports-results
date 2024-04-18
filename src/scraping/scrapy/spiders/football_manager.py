import asyncio
from pathlib import Path

import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod

from src.scraping.scrapy.utils import clean_key, playwright_save_page, try_convert


class FootballManagerSpider(scrapy.Spider):
    name = "football_manager"
    allowed_domains = ["fminside.net"]
    # start_urls = ["https://fminside.net/clubs"]
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_HEADLESS": False,  # Cambiar a True para no mostrar navegador
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    # Crea la carpeta logs si no existe
    def __init__(self, *args, **kwargs):
        super(FootballManagerSpider, self).__init__(*args, **kwargs)
        Path("logs").mkdir(parents=True, exist_ok=True)

    def start_requests(self):
        urls = ["https://fminside.net/clubs"]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True, "playwright_include_page": True})

    # Paso 1: Ingresar la liga y obtener todos los clubes
    async def parse(self, response):
        page = response.meta["playwright_page"]
        # await page.evaluate("document.body.style.zoom = '75%'")
        # await page.screenshot(path="logs/pagina_inicio.png")
        # TODO: Podemos obtener todas las ligas de: "//div[@class="leagues"]/ul/li/a/text()"
        await page.type('//form//div//input[@placeholder="League"]', "LaLiga")
        await page.keyboard.press("Enter")
        await page.wait_for_selector('//div[@class="active-filter" and text()="League: LaLiga"]')
        await page.wait_for_timeout(2000)
        # await page.screenshot(path="logs/league_LaLiga.png")
        club_elements = await page.query_selector_all('xpath=//ul[@class="club"]/li/span[2]/b/a')
        #club_elements = club_elements[:1]  # ! Descomentar para probar
        if club_elements == []:
            self.logger.error("No se encontraron clubes")
            await playwright_save_page(page, "logs/error_club.html")
        else:
            for club in club_elements:
                yield scrapy.Request(
                    f"https://fminside.net/{await club.get_attribute('href')}",
                    callback=self.parse_club,
                    meta={"playwright": True, "playwright_include_page": True},
                )
        await page.close()

    # # Paso 2: Recorrer cada club y obtener todos los jugadores
    async def parse_club(self, response):
        page = response.meta["playwright_page"]
        await page.evaluate("document.body.style.zoom = '55%'")
        # await page.screenshot(path=f"logs/{response.url.split('/')[-1]}.png")
        # await playwright_save_page(page, f"logs/{response.url.split('/')[-1]}.html")
        player_elements = await page.query_selector_all('//li[@class="player"]/span/b/a')
        hrefs = [await player.get_attribute("href") for player in player_elements]
        player_urls = set(hrefs)
        # player_urls = list(player_urls)[:1]  # ! Descomentar para probar
        if len(player_urls) == 0:
            self.logger.error(f"No se encontraron jugadores en {response.url}")
            await playwright_save_page(page, "logs/error_jugador.html")
        else:
            for url in player_urls:
                yield scrapy.Request(
                    f"https://fminside.net{url}",
                    callback=self.parse_player,
                )
        await page.close()

    # # Paso 3: Recorrer cada jugador y obtener sus estadísticas
    async def parse_player(self, response):
        # with open("logs/player.html", "w") as f:
        #     f.write(response.text)
        data = self.extract_player_data(Selector(text=response.text))
        yield data

    def extract_player_data(self, selector):  # noqa: C901
        player = {}
        player["name"] = selector.xpath('//div[@id="player"]/div[@class="title"]/h1/text()').get()
        player["ability"] = int(selector.xpath('//span[@id="ability"]/text()').get() or 0)
        player["potential"] = int(selector.xpath('//span[@id="potential"]/text()').get() or 0)
        player["club"] = selector.xpath('//*[@id="player"]/div[1]/div/ul/li[1]/a/span[2]/text()').get()
        player["country"] = selector.xpath('//*[@id="player"]/div[1]/div/ul/li[2]/span/a/text()').get()

        # Extracción de información detallada de la sección de 'Player Info'
        info_items = selector.xpath('//div[@id="player_info"]//div[@class="column"][1]//li')
        for item in info_items:
            key = item.xpath("./span[1]/text()").get()
            if key:
                key = clean_key(key)
                if key == "positions":
                    value = item.xpath("./span[2]/span[1]/span[1]/text()").get()
                    player["natural"] = value
                    player["accomplished"] = item.xpath("./span[2]/span[1]/span[2]/text()").get()
                else:
                    player[key] = item.xpath("./span[2]/text()").get()

        # Extracción de información del contrato
        contract_items = selector.xpath('//div[@id="player_info"]//div[@class="column"][2]//li')
        for item in contract_items:
            key = item.xpath("./span[1]/text()").get()
            if key:
                key = clean_key(key)
                player[key] = item.xpath("./span[2]/text()").get()

        # Extracción de roles adecuados
        roles = selector.xpath('//ol[@id="suitable"]/li')
        for i, role in enumerate(roles):
            if i < len(roles) - 1:
                key = role.xpath("./span[1]/text()").get()
                value = role.xpath("./span[2]/text()").get()
                if key and value.strip():
                    key = clean_key(key)
                    player[key] = try_convert(value, float)
            else:
                options = role.xpath("./select/option/text()").getall()
                for option in options:
                    key, value = option.split(" - ")
                    key = clean_key(key)
                    player[key] = try_convert(value.strip(), float)

        # Extracción de atributos
        attributes = selector.xpath('//*[@id="player_stats"]/div/table/tr')
        for attribute in attributes:
            key = attribute.xpath(".//td[1]/acronym/text()").get()
            value = attribute.xpath('.//td[2]/text()').get()
            if key and value:
                key = clean_key(key)
                player[key] = try_convert(value.strip(), int)

        return player

