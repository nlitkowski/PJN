# -*- coding: utf-8 -*-
import scrapy


class FilmsSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = [
        "https://www.booking.com/searchresults.html?aid=356980&label=gog235jc-1FCAIoZTgeSDNYA2i2AYgBAZgBHrgBF8gBD9gBAegBAfgBDIgCAagCA7gCmdi38QXAAgE&lang=en-us&sid=4b6e6172852ffec7cbc17bd7cfcd652a&sb=1&sb_lp=1&src=country&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fcountry%2Fhr.html%3Faid%3D356980%3Blabel%3Dgog235jc-1FCAIoZTgeSDNYA2i2AYgBAZgBHrgBF8gBD9gBAegBAfgBDIgCAagCA7gCmdi38QXAAgE%3Bsid%3D4b6e6172852ffec7cbc17bd7cfcd652a%3Binac%3D0%3Bsrpvid%3D6adf8aedb1e600b6%26%3B&sr_autoscroll=1&ss=Croatia&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=Croa&ac_position=0&ac_langcode=en&ac_click_type=b&dest_id=54&dest_type=country&place_id_lat=44.7185&place_id_lon=16.145&search_pageview_id=21948b58e003010f&search_selected=true&search_pageview_id=21948b58e003010f&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"
    ]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        for hotel_div in response.xpath("//div[@class='sr-hotel__title-wrap']"):
            hxs = scrapy.selector.Selector(text=hotel_div.extract())
            hotel_name = hxs.xpath("//span[@class='sr-hotel__name']/text()").get()
            hotel_link = hxs.xpath("//a[@class='hotel_name_link url']/@href").get()
            yield scrapy.Request(
                hotel_link,
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
        if text_eng is None:
            t = response.xpath("//a[@rel='v:starring']/text()").getall()
            text_eng = ""
            hr_link = response.xpath("//a[@rel='v:starring']/text()").get()
            return scrapy.Request(
                hr_link,
                callback=self.parse_hotel,
                cb_kwargs={"name": name, "text_eng": text_eng, "text_hr": None},
            )
        else:
            text_hr = ""
            if text_hr != text_eng:
                return {"name": name, "text_eng": text_eng, "text_hr": text_hr}
            else:
                return None
