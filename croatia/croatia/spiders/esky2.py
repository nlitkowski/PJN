# -*- coding: utf-8 -*-
import scrapy


class EskySpider(scrapy.Spider):
    name = "esky-brutal"
    allowed_domains = ["esky.hr", "esky.com"]
    base_url = "https://www.esky.hr"
    iteration = 1
    start_urls = [
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
        "https://www.esky.hr/",
    ]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        for i in range(self.iteration * 100000, (self.iteration + 1) * 100000):
            yield scrapy.Request(
                f"{self.base_url}/hoteli/ho/{i}",
                callback=self.parse_hotel,
                cb_kwargs={"name": i, "text_eng": None, "text_hr": None},
            )
        self.iteration += 1

    def parse_hotel(
        self, response: scrapy.http.response.html.HtmlResponse, name, text_eng, text_hr
    ):
        if text_hr is None:
            text_hr = "".join(
                response.xpath("//dd[@class='hotel-description']//text()").extract()
            )
            if text_hr == "":
                return None
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
