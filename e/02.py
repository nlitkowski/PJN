import json


def main():
    text_json = json.load(open("e01/nlp.json"))
    for d in text_json:
        print(d[1])


if __name__ == "__main__":
    main()
