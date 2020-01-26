import json
from nltk.tokenize import sent_tokenize
from subprocess import run


def main():
    text_json = json.load(open("out4.json"))
    for x in text_json:
        process(x)
    # scripts working on Windows cmd
    run('echo "" > tmp.dict', shell=True)
    run("hunalign -text -utf -realign tmp.dict hr.txt en.txt > aligned.txt", shell=True)
    run("del hr.txt en.txt tmp.dict translate.txt", shell=True)


def process(x):
    with open("hr.txt", mode="a", encoding="utf-8") as f:
        for l in sent_tokenize(x["text_hr"]):
            f.write(l.strip() + "\n")
    with open("en.txt", mode="a", encoding="utf-8") as f:
        for l in sent_tokenize(x["text_eng"]):
            f.write(l.strip() + "\n")


if __name__ == "__main__":
    main()
