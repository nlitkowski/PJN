import json
from nltk.tokenize import sent_tokenize


def main():
    text_json = json.load(open("e01/nlp.json"))
    for x in text_json:
        for y in text_json:
            if x != y and (x["site"]).replace(".php", "_en.php") == y["site"]:
                process(x, y)


def process(s1, s2):
    token_list1 = sent_tokenize(s1["text"])
    token_list2 = sent_tokenize(s2["text"])


if __name__ == "__main__":
    main()
