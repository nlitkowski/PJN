# -*- coding: utf-8 -*-
import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["filmweb.pl"]
    base_domain = "https://www.filmweb.pl"
    start_urls = [
        "https://www.filmweb.pl/films/search?orderBy=popularity&descending=true&page=1"
    ]
    repeats = 0
    max_repeats = 999  # 1001st page doesnt exist

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        for film_li in response.xpath("//li[@class='hits__item']"):
            hxs = scrapy.selector.Selector(text=film_li.extract())
            link = hxs.xpath("//a[@class='filmPreview__link']/@href").get()
            grade = hxs.xpath("//span[@class='rateBox__rate']/text()").get()
            grade_count = hxs.xpath(
                "//span[@class='rateBox__votes rateBox__votes--count']/text()"
            ).get()
            if grade is not None:
                yield scrapy.Request(
                    self.base_domain + link + "/cast/actors",
                    callback=self.parse_cast,
                    cb_kwargs={
                        "grade": float(grade.replace(",", ".")),
                        "count": int(grade_count.strip().replace(" ", "")),
                        "actors": None,
                    },
                )
        if self.repeats < self.max_repeats:
            self.repeats += 1
            print(f"URL: <{response._get_url()}>")
            yield response.follow(
                "/films/search"
                + response.xpath(
                    "//li[@class='pagination__item pagination__item--next']/a/@href"
                ).get()
            )

    def parse_cast(
        self, response: scrapy.http.response.html.HtmlResponse, grade, count, actors
    ):
        cast_list = response.xpath("//a[@rel='v:starring']/text()").getall()
        if actors is None:
            return scrapy.Request(
                response._get_url().replace("actors", "crew"),
                callback=self.parse_cast,
                cb_kwargs={"grade": grade, "count": count, "actors": cast_list},
            )
        else:
            return {"grade": grade, "count": count, "actors": actors, "crew": cast_list}

