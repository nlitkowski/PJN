from sys import argv
from bs4 import BeautifulSoup, Tag
import requests


class Team:
    def __init__(self, result: int, name: str):
        self.result = result
        self.name = name


def d02():
    website_base = "https://pl.wikipedia.org/wiki/Ekstraklasa_w_pi%C5%82ce_no%C5%BCnej_"
    seasons = [f"({i}/{i + 1})" for i in range(2008, 2019)]
    sources = [get_source(website_base + s) for s in seasons]

    res_dict = {}

    for s in sources:
        parse_html(s, res_dict)

    results = [Team(res_dict[x], x) for x in res_dict]
    create_out_table(results)


def get_source(site: str):
    req = requests.get(site)
    return req.text


def parse_html(source: str, res_dict: dict):
    bs = BeautifulSoup(source, features="html.parser")
    span = bs.find("span", id="Tabela_2")

    if span is None:
        span = bs.find("span", id="Tabela")

    rows = span.parent.find_next_siblings("table")[0].tbody.find_all("tr")

    for i in range(1, len(rows)):
        tds = rows[i].find_all("td")
        if len(tds) > 1:
            try:
                res_dict[tds[1].a.text] += int(tds[9].b.text)
            except KeyError:
                res_dict[tds[1].a.text] = int(tds[9].b.text)


def create_out_table(results: list):
    bs = BeautifulSoup(
        open("table.template.html"), features="html.parser", from_encoding="utf-8"
    )
    i = 1
    row = BeautifulSoup(
        "<tr><td>l.p.</td>Drużyna<td></td><td>Wynik</td></tr>", features="html.parser"
    )
    bs.html.body.table.thead.append(row)
    for x in sorted(results, key=lambda x: x.result, reverse=True):
        row = BeautifulSoup(
            f"<tr><td>{i}</td><td>{x.name}</td><td>{x.result}</td></tr>",
            features="html.parser",
        )
        bs.html.body.table.tbody.append(row)
        i += 1
    with open("table.html", encoding="utf-8", mode="w") as f:
        f.write(str(bs))


if __name__ == "__main__":
    d02()


"""
Zawartość plku table.template.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta content="text/html" />
    <meta http-equiv="Content-type" />
    <title>Table</title>
  </head>
  <body>
    <table>
      <thead></thead>
      <tbody></tbody>
    </table>
  </body>
</html>
"""
