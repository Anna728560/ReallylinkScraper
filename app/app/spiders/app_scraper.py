import scrapy


class AppScraperSpider(scrapy.Spider):
    name = "app_scraper"
    allowed_domains = ["realtylink.org"]
    start_urls = ["https://realtylink.org/en/properties~for-rent?uc=0"]

    def parse(self, response):
        pass
