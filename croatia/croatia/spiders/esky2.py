# -*- coding: utf-8 -*-
import scrapy


class EskySpider(scrapy.Spider):
    name = "esky-brutal"
    allowed_domains = ["esky.hr", "esky.com"]
    base_url = "https://www.esky.hr"
    start_urls = [f"https://www.esky.hr/hoteli/ho/{i}" for i in range(100000, 999999)]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        text_hr = "".join(
            response.xpath("//dd[@class='hotel-description']//text()").extract()
        )
        if text_hr == "":
            return None
        new_link = response._get_url().replace("esky.hr/hoteli", "esky.com/hotels")
        return scrapy.Request(
            new_link, callback=self.parse_eng, cb_kwargs={"text_hr": text_hr}
        )

    def parse_eng(self, response: scrapy.http.response.html.HtmlResponse, text_hr: str):
        text_eng = "".join(
            response.xpath("//dd[@class='hotel-description']//text()").extract()
        )
        if text_hr != text_eng:
            with open("c_output_hr.txt", "a", encoding="utf-8") as f:
                f.write(text_hr.replace("\t", "").replace("\n", ""))
            with open("c_output_en.txt", "a", encoding="utf-8") as f:
                f.write(text_eng.replace("\t", "").replace("\n", ""))

