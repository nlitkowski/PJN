# -*- coding: utf-8 -*-
import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["filmweb.pl"]
    base_domain = "https://www.filmweb.pl"
    start_urls = [
        "https://www.filmweb.pl/films/search?orderBy=popularity&descending=true&page=1"
    ]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        for film_div in response.xpath("//a[@class='filmPreview__link']/@href"):
            link = film_div.xpath("//a[@class='filmPreview__link']/@href").get()
            grade = film_div.xpath("//span[@class='rateBox__rate']/text()").get()
            yield scrapy.Request(
                self.base_domain + link,
                callback=self.parse_film,
                cb_kwargs={"grade": float(grade)},
            )
        yield response.follow(
            "/films/search"
            + response.xpath(
                "//li[@class='pagination__item pagination__item--next']/a/@href"
            ).get()
        )

    def parse_film(self, response: scrapy.http.response.html.HtmlResponse):
        grade = response.cb_kwargs["grade"]
        crew = scrapy.Request(
            response._get_url() + "/cast/crew", callback=self.parse_crew
        )
        actors = scrapy.Request(
            response._get_url() + "/cast/actors", callback=self.parse_actors
        )
        yield {"grade": grade, "actors": actors, "crew": crew}

    def parse_crew(self, response: scrapy.http.response.html.HtmlResponse):
        pass

    def parse_actors(self, response: scrapy.http.response.html.HtmlResponse):
        pass
