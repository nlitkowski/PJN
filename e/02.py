import json
from nltk.tokenize import sent_tokenize
from subprocess import run


def main():
    text_json = json.load(open("e01/nlp.json"))
    for x in text_json:
        for y in text_json:
            if x != y and (x["site"]).replace(".php", "_en.php") == y["site"]:
                process(x, y)
    run("touch tmp.dict")
    run("hunalign -text -utf -realign tmp.dict pl.txt en.txt > aligned.txt")


def process(pl, en):
    with open("pl.txt", mode="a", encoding="utf-8") as f:
        f.writelines(sent_tokenize(pl["text"]))
    with open("en.txt", mode="a", encoding="utf-8") as f:
        f.writelines(sent_tokenize(en["text"]))


if __name__ == "__main__":
    main()
