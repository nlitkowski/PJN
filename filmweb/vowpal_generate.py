import json
from encodings import utf_8


def main():
    with open("out.json") as f:
        json_loaded = json.load(f)
    length = len(json_loaded)
    # Divide data into sets of appropriate size
    learning_set = json_loaded[: round(length * 0.8)]
    dev_set = json_loaded[
        round(length * 0.8) : round(length * 0.8) + round(length * 0.1)
    ]
    test_set = json_loaded[round(length * 0.8) + round(length * 0.1) :]

    with open("learn_data.txt", "w", encoding="utf-8") as f:
        for o in learning_set:
            f.write(get_vw_line_train(o))

    with open("dev_data.txt", "w", encoding="utf-8") as f:
        for o in dev_set:
            f.write(get_vw_line_test(o))

    with open("test_data.txt", "w", encoding="utf-8") as f:
        for o in dev_set:
            f.write(get_vw_line_test(o))


def get_vw_line_train(o):
    """o: json object representing Filmweb data"""

    crew_string = ""
    for l in o["crew"]:
        crew_string += f"crew_{l.strip().replace(' ', '_')} "

    actors_string = ""
    for l in o["actors"]:
        actors_string += f"actor_{l.strip().replace(' ', '_')} "
    # result importance | features
    return f"{o['grade']} {o['count']} | {crew_string} {actors_string}\n"

def get_vw_line_test(o):
        """o: json object representing Filmweb data"""

    crew_string = ""
    for l in o["crew"]:
        crew_string += f"crew_{l.strip().replace(' ', '_')} "

    actors_string = ""
    for l in o["actors"]:
        actors_string += f"actor_{l.strip().replace(' ', '_')} "

    return f"| {crew_string} {actors_string}\n"

if __name__ == "__main__":
    main()
