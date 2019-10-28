from re import match


def b01():
    name = input("Imię: ")
    if not match(r"^[A-Z].+$", name):
        print("Imię musi zaczynać się wielką literą")
    surname = input("Nazwisko: ")
    if not match(r"^[A-Z].+$", surname):
        print("Litkowski musi zaczynać się wielką literą")
    city = input("Miasto: ")
    if not match(r"^[A-Z].+$", city):
        print("Miasto musi zaczynać się wielką literą")
    postcode = input("Kod pocztowy: ")
    if not match(r"^\d{2}\-\d{3}$", postcode):
        print("Kod pocztowy musi być w formacie '11-111'")
    phone = input("Telefon: ")  # (61) 222-45-56
    if not match(r"^\([0-9]{2}\)\s\d{3}\-\d{2}\-\d{2}$", phone):
        print("Telefon musi być w formacie '(61) 222-45-56'")


if __name__ == "__main__":
    b01()
