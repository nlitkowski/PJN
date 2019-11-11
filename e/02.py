import json
from nltk.tokenize import sent_tokenize
from subprocess import run


def main():
    text_json = json.load(open("e01/nlp.json"))
    for x in text_json:
        for y in text_json:
            if x != y and (x["site"]).replace(".php", "_en.php") == y["site"]:
                process(x, y)
    run('echo "" > tmp.dict', shell=True)
    run("hunalign -text -utf -realign tmp.dict pl.txt en.txt > aligned.txt", shell=True)
    run("rm en.txt pl.txt tmp.dict translate.txt", shell=True)


def process(pl, en):
    with open("pl.txt", mode="a", encoding="utf-8") as f:
        for l in sent_tokenize(pl["text"]):
            f.write(l)
    with open("en.txt", mode="a", encoding="utf-8") as f:
        for l in sent_tokenize(en["text"]):
            f.write(l)


if __name__ == "__main__":
    main()
