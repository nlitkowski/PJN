# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.spiders.crawl import CrawlSpider
import time


class EskySpider(CrawlSpider):
    name = "esky-hr"
    allowed_domains = ["esky.hr", "esky.com"]
    base_url = "https://www.esky.hr"
    start_urls = ["https://www.esky.hr/hoteli/ci/spu/hoteli-split"]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        self.browser.get(response.url)
        time.sleep(3)
        body_hxs = scrapy.selector.Selector(text=self.browser.page_source)
        for hotel_div in body_hxs.xpath("//div[@class='hotel-offer-wrapper']"):
            hxs = scrapy.selector.Selector(text=hotel_div.extract())
            hotel_name = hxs.xpath("//li[@class='hotel-name']/a/span/text()").get()
            hotel_link = hxs.xpath(
                "//li[@class='hotel-name']/a[@class='name-link']/@href"
            ).get()
            yield scrapy.Request(
                self.base_url + hotel_link,
                callback=self.parse_hotel,
                cb_kwargs={"name": hotel_name, "text_eng": None, "text_hr": None},
            )

        next_page_link = response.xpath(
            "//a[@class='bui-pagination__link paging-next']/@href"
        ).get()
        if next_page_link is not None:
            yield response.follow(next_page_link)

    def parse_hotel(
        self, response: scrapy.http.response.html.HtmlResponse, name, text_eng, text_hr
    ):
        if text_hr is None:
            text_hr = "".join(
                response.xpath("//dd[@class='hotel-description']//text()").extract()
            )
            new_link = response._get_url().replace("esky.hr/hoteli", "esky.com/hotels")
            return scrapy.Request(
                new_link,
                callback=self.parse_hotel,
                cb_kwargs={"name": name, "text_eng": None, "text_hr": text_hr},
            )
        else:
            text_eng = "".join(
                response.xpath("//dd[@class='hotel-description']//text()").extract()
            )
            if text_hr != text_eng:
                return {
                    "name": name,
                    "text_eng": text_eng.strip(),
                    "text_hr": text_hr.strip(),
                }
            else:
                return None
