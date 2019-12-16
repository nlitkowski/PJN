# -*- coding: utf-8 -*-
import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["filmweb.pl"]
    base_domain = "https://www.filmweb.pl"
    start_urls = [
        "https://www.filmweb.pl/films/search?endYear=2019&orderBy=popularity&descending=true&startYear=1960&page=1"
    ]
    repeats = 0
    max_repeats = 999  # 1001st page doesnt exist

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        for film_li in response.xpath("//li[@class='hits__item']"):
            hxs = scrapy.selector.Selector(text=film_li.extract())
            link = hxs.xpath("//a[@class='filmPreview__link']/@href").get()
            grade = hxs.xpath("//span[@class='rateBox__rate']/text()").get()
            year = hxs.xpath("//span[@class='filmPreview__year']/text()").get()
            original_title = hxs.xpath(
                "//div[@class='filmPreview__originalTitle']/text()").get()
            title = hxs.xpath("//h3[@class='filmPreview__title']/text()").get()
            genre = hxs.xpath(
                "//div[@class='filmPreview__info filmPreview__info--genres']/ul/li/a/text()").get()
            director = hxs.xpath(
                "//div[@class='filmPreview__info filmPreview__info--directors']/ul/li/a/text()").get()
            country = hxs.xpath(
                "//div[@class='filmPreview__info filmPreview__info--countries']/ul/li/a/text()").get()
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
                        "year": year,
                        "original_title": original_title,
                        "title": title,
                        "genre": genre,
                        "director": director,
                        "country": country,
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
        self, response: scrapy.http.response.html.HtmlResponse, grade, count, year, original_title, title, genre, director, country, actors
    ):
        cast_list = response.xpath("//a[@rel='v:starring']/text()").getall()
        if actors is None:
            return scrapy.Request(
                response._get_url().replace("actors", "crew"),
                callback=self.parse_cast,
                cb_kwargs={"grade": grade, "count": count, "year": year, "original_title": original_title,
                           "title": title,
                           "genre": genre,
                           "director": director,
                           "country": country, "actors": cast_list},
            )
        else:
            return {"grade": grade, "count": count, "year": year, "original_title": original_title,
                    "title": title,
                    "genre": genre,
                    "director": director,
                    "country": country, "actors": actors, "crew": cast_list}
