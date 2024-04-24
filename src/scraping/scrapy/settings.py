
BOT_NAME = "scrapy"

SPIDER_MODULES = ["src.scraping.scrapy.spiders"]
NEWSPIDER_MODULE = "src.scraping.scrapy.spiders"

ROBOTSTXT_OBEY = True
DUPEFILTER_DEBUG = True  # permite solicitudes duplicadas


LOG_LEVEL = "INFO"  # INFO OR ERROR OR DEBUG OR CRITICAL
DOWNLOAD_DELAY = 0.2
DOWNLOAD_TIMEOUT = 360
TELNETCONSOLE_ENABLED = False
USER_AGENT = "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188"

COOKIES_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# Playwright settings
PLAYWRIGHT_ABORT_REQUEST = "src.scraping.scrapy.utils.should_abort_request" # funcion para no cargar request innecesarias

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_CONCURRENCY = 10
PLAYWRIGHT_MAX_CONTEXTS = 8
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 8
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 400000  # None  # 200 * 1000
