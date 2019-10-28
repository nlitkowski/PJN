from b01 import b01
from b02 import b02
from b03 import b03
from b04 import b04


def loop(task):
    if task == 1:
        b01()
    elif task == 2:
        b02()
    elif task == 3:
        b03()
    elif task == 4:
        b04()


if __name__ == "__main__":
    while True:
        try:
            print("Które zadanie chcesz zobaczyć? Wybierz numer 1-4")
            task = int(input("Numer: "))
        except (Exception):
            break
        if task in (1, 2, 3, 4):
            loop(task)
        else:
            break

