import json
from datetime import datetime

OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers, products, customers):
    for i, customer in enumerate(customers, 1):
        print(f"{i}. {customer['name']}")
    customer = customers[int(input("Odaberite kupca: ")) - 1]
    # Unos datuma 
    date = input("Unesite datum (YYYY-MM-DD, Enter za danas): ") or datetime.today().strftime('%Y-%m-%d')
    # Odabir proizvoda
    items = []
    for i, product in enumerate(products, 1):
        print(f"{i}. {product['name']} - {product['price']} EUR")
    while (choice := input("Odaberite proizvod (Enter za kraj): ")):
        product = products[int(choice) - 1]
        quantity = int(input("Količina: "))
        items.append({"product": product, "quantity": quantity})
    # Ako nema proizvoda, prekini
    if not items:
        print("Ponuda mora imati barem jedan proizvod!")
        return
    # Izračunaj ukupne troškove
    sub_total = sum(item["product"]["price"] * item["quantity"] for item in items)
    tax, total = sub_total * 0.25, sub_total * 1.25  
    # Dodaj ponudu u listu
    offers.append({"customer": customer, "date": date, "items": items, "sub_total": sub_total, "tax": tax, "total": total})
    print(f"\nPonuda kreirana, Ukupno: {total:.2f} EUR")


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    """
    Allows the user to add a new product or modify an existing product.
    """
    choice = int(input("Stisni 1 za izmjenu ili 2 za dodavanje novog proizvoda: "))
    if choice == 1:
        print("ovo su svi dostupni proizvodi")
        for product in products:
            print(f"{product['id']}. {product['name']} - {product['price']} EUR")
        id_of_choice = int(input("Odaber id za izmjenu odredenog proizvoda ako zelis napravit promjene za njega: "))
        for s in products:
            if s["id"] == int(id_of_choice):
                product = s
                new_name = str(input("Upisi novo ime proizvoda:"))
                new_description = str(input("Upisi novi opis proizvoda: "))
                new_price = float(input("Upisi novu cijenu proizvoda:"))
                product['name'] = new_name
                product['description'] = new_description
                product['price'] = new_price
                print("Ovo su upisani podaci za " + product["name"]+ ", " + new_name + ", " + new_description + ", " + str(new_price))
    elif choice == 2:
        print("Dodavanje novog proizvoda:")
        print()
        name = str(input("Ime proizvoda kopjeg zelis dodati: "))
        description = str(input("Opis proizvoda: "))
        price = float(input("Cijena proizvoda: "))
        maks_id = max(product["id"] for product in products)
        new_id = maks_id + 1
        products.append({"id": new_id, "name": name, "description": description, "price": price})
        print("\nAžurirani proizvodi:")
        for product in products:
            print(f"{product['id']}. {product['name']} - {product['price']} EUR")
    else:
        print("error: ovaj izbor ne postoji")

    
    
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    


# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers):
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca
    choice = int(input("Za dodavanje novog kupca i njegovih podataka unesi 1 a za pregled svih kupaca 2:"))
    if choice == 1:
        name = str(input("Ime novog kupca: "))
        email = str(input("Email kupca: "))
        vat_id = int(input("Novi vat id: "))
        customers.append({"name": name, "email": email, "vat_id": vat_id})
        print("Podaci uneseni za novog customera: " + name  + ", " + email + ", " + str(vat_id ))
    elif choice == 2:
        print("Lista svih kupaca: ")
        print()
        for customer in customers:
            print(f"Customer name: {customer['name']}")
            print(f"Email: {customer['email']}")
            print(f"VAT ID: {customer['vat_id']}")

    else: 
        print("Ovaj izbor ne postoji")


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora
    choice = int(input("Stisni 1 za prikaz svih ponuda, 2 za prikaz ponuda po mjesecu i 3 za prikaz ponuda po IDu: "))
    if choice == 1:
        for offer in offers:
            print(f"Ponuda {offer['offer_number']} za {offer['customer']} na datum: {offer['date']}")
            for item in offer['items']:
                print(f" {item['product_name']} - {item['price']} EUR x {item['quantity']} = {item['item_total']} EUR")
    elif choice == 2:
        month = int(input("Mjesec po kojem zelis pretraziti ponude(unesi u broju, npr. 11): "))
        for offer in offers:
            offer_date = datetime.strptime(offer['date'], '%Y-%m-%d')
            if offer_date.month == int(month):
                print(f"Offer {offer['offer_number']} for {offer['customer']} on {offer['date']}")
                for item in offer['items']:
                    print(f"{item['product_name']} x{item['quantity']} - {item['price'] * item['quantity']} EUR")
                else:
                    print("nema ponuda za ovaj mjesec")
    elif choice == 3:
        offer_number_to_find = 1  # Traženi ID ponude

        # Pretraga po ID-u
        found_offer = next((offer for offer in offers if offer['offer_number'] == offer_number_to_find), None)
        if found_offer:
            print("Ponuda pronađena:\n")
            print(f"ID ponude: {found_offer['offer_number']}")
            print(f"Kupac: {found_offer['customer']}")
            print(f"Datum: {found_offer['date']}")
            print("\nProizvodi u ponudi:")
            for item in found_offer['items']:
                print(f"- {item['product_name']} ({item['description']}): {item['quantity']} x {item['price']} = {item['item_total']}")
                print(f"\nSubtotal: {found_offer['sub_total']}")
                print(f"PDV: {found_offer['tax']}")
                print(f"Ukupno: {found_offer['total']}")
            else:
                print(f"Ponuda sa ID {offer_number_to_find} nije pronađena.")

                    




# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']['name']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()
