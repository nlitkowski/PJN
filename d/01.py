from sys import argv
from bs4 import BeautifulSoup
import requests


def d01(
    start_website="https://www.ceneo.pl/Szlifierki_i_polerki;szukaj-szlifierka+k%c4%85towa#catnarrow=1"
):
    filename = "output.txt"

    products = []
    (p, href) = parse_html(get_source(start_website))
    products.extend(p)
    while href is not None:
        (p, href) = parse_html(get_source("https://www.ceneo.pl/" + href))
        products.extend(p)
    with open(filename, "w") as fd:
        for p in products:
            fd.write(f"{p}\n")
    print(f"Found {len(products)} products.")
    print(f"Saved them to {filename}")


def get_source(site):
    req = requests.get(site)
    return req.text


def parse_html(source):
    bs = BeautifulSoup(source, features="html.parser")

    products = [
        p.a.text
        for p in bs.find("section", class_="category-list")
        .find("div", class_="category-list-body")
        .find_all("strong", class_="cat-prod-row-name")
    ]

    next_page = bs.find("li", class_="page-arrow arrow-next")

    if next_page is not None:
        return products, next_page.a["href"]
    return products, None


if __name__ == "__main__":
    if len(argv) > 1:
        d01(argv[1])
    else:
        d01()
