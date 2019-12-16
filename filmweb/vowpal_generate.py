import json
from encodings import utf_8


def main():
    with open("out.json") as f:
        json_loaded = json.load(f)
    length = len(json_loaded)
    # Divide data into sets of appropriate size
    learning_set = json_loaded[: round(length * 0.8)]
    dev_set = json_loaded[
        round(length * 0.8): round(length * 0.8) + round(length * 0.1)
    ]
    test_set = json_loaded[round(length * 0.8) + round(length * 0.1):]

    with open("learn_data.txt", "w", encoding="utf-8") as f:
        for o in learning_set:
            f.write(get_vw_line_train(o))

    with open("dev_data.txt", "w", encoding="utf-8") as f:
        with open("dev_data_actual.txt", "w") as f2:
            for o in dev_set:
                line_data, line_actual = get_vw_line_test(o)
                f.write(line_data)
                f2.write(line_actual)

    with open("test_data.txt", "w", encoding="utf-8") as f:
        with open("test_data_actual.txt", "w") as f2:
            for o in test_set:
                line_data, line_actual = get_vw_line_test(o)
                f.write(line_data)
                f2.write(line_actual)


def get_vw_line_train(o):
    """o: json object representing Filmweb data"""

    crew_string = ""
    for l in o["crew"]:
        crew_string += f"crew_{l.strip().replace(' ', '_')} "

    title_string = o['title'].strip()
    ori_title_string = o['original_title'].strip()
    director = 'director_' + o['director'].replace(' ', '_')
    actors_string = ""
    for l in o["actors"]:
        actors_string += f"actor_{l.strip().replace(' ', '_')} "
    # result importance | features
    return f"{o['grade']} {o['count']} | {director} {ori_title_string} {title_string} year_{o['year']} genre_{o['genre'].replace(' ', '_')} country_{o['country'].replace(' ','_')} {crew_string} {actors_string}\n"


def get_vw_line_test(o):
    """o: json object representing Filmweb data"""

    crew_string = ""
    for l in o["crew"]:
        crew_string += f"crew_{l.strip().replace(' ', '_')} "

    actors_string = ""
    for l in o["actors"]:
        actors_string += f"actor_{l.strip().replace(' ', '_')} "

    title_string = o['title'].strip()
    ori_title_string = o['original_title'].strip()
    director = 'director_' + o['director'].replace(' ', '_')

    return f"| {director} {ori_title_string} {title_string} year_{o['year']} genre_{o['genre'].replace(' ', '_')} country_{o['country'].replace(' ','_')} {crew_string} {actors_string}\n", f"{o['grade']}\n"


if __name__ == "__main__":
    main()
