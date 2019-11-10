import scrapy
import re


class NlpSpider(scrapy.Spider):
    name = "nlp"
    start_urls = ["http://rjawor.home.amu.edu.pl/index.php"]
    visited = ["index.php"]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        text = "".join(response.xpath("//body//text()").extract())
        text = text.replace("\t", " ").replace("\n", " ")
        # text = re.sub(r"\s+", " ", text)
        yield {f"Text at '{response._get_url()}'": text}
        hrefs = []
        for link in response.xpath("//a/@href").getall():
            hrefs.append(link)
        if len(hrefs) > 0:
            home_redirect = re.compile(r"[a-zA-Z_]+\.php")
            for l in hrefs:
                if home_redirect.match(l) and l not in self.visited:
                    self.visited.append(l)
                    yield response.follow(l, callback=self.parse)

