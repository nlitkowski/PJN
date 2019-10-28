from re import compile


def b02():
    regex = compile(r"^[a-zA-Z]+;\d+;\d+$")
    with open("b02-test.csv", "r") as f:
        for line in f:
            if not regex.match(line):
                print(f"Line invalid: {line}")
                # break


if __name__ == "__main__":
    b02()


"""
Zawartość pliku b02-test.csv
test;214;124
asoda;22141;111
1245;124d;as
1241255;safa104125;;5521
124;123.23;4214,421
asd;3.3;2
"""

