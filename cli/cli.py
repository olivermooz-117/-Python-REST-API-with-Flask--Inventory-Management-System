"""
CLI frontend for the Inventory Management System.

Talks to the Flask API over HTTP (via `requests`), the same way any
external client would. Run the Flask server first (`python run.py`),
then run this CLI in a separate terminal (`python -m cli.cli`).

Each action is its own function so it can be unit tested independently
by mocking `requests`.
"""

import requests

BASE_URL = "http://localhost:5000/inventory"


# ---- API-calling functions (the "logic" layer, easy to unit test) ---------

def list_items():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()


def view_item(item_id):
    response = requests.get(f"{BASE_URL}/{item_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def add_item(product_name, brand="", quantity=0, price=0.0):
    payload = {
        "product_name": product_name,
        "brand": brand,
        "quantity": quantity,
        "price": price,
    }
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()
    return response.json()


def update_item(item_id, **fields):
    response = requests.patch(f"{BASE_URL}/{item_id}", json=fields)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/{item_id}")
    if response.status_code == 404:
        return False
    response.raise_for_status()
    return True


def find_on_api(barcode=None, name=None):
    params = {}
    if barcode:
        params["barcode"] = barcode
    if name:
        params["name"] = name
    response = requests.get(f"{BASE_URL}/lookup", params=params)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def add_item_from_barcode(barcode, quantity=0, price=0.0):
    payload = {"barcode": barcode, "quantity": quantity, "price": price}
    response = requests.post(f"{BASE_URL}/lookup", json=payload)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


# ---- Menu / presentation layer ---------------------------------------------

MENU = """
Inventory Management CLI
1. View all inventory items
2. View a single item
3. Add a new item manually
4. Add a new item by barcode (via OpenFoodFacts)
5. Update item price/stock
6. Delete an item
7. Search OpenFoodFacts by product name
8. Exit
"""


def run():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                for item in list_items():
                    print(item)

            elif choice == "2":
                item_id = int(input("Item ID: "))
                item = view_item(item_id)
                print(item if item else "Item not found.")

            elif choice == "3":
                name = input("Product name: ")
                brand = input("Brand: ")
                quantity = int(input("Quantity: ") or 0)
                price = float(input("Price: ") or 0.0)
                print(add_item(name, brand, quantity, price))

            elif choice == "4":
                barcode = input("Barcode: ")
                quantity = int(input("Quantity: ") or 0)
                price = float(input("Price: ") or 0.0)
                result = add_item_from_barcode(barcode, quantity, price)
                print(result if result else "No product found for that barcode.")

            elif choice == "5":
                item_id = int(input("Item ID to update: "))
                price = input("New price (leave blank to skip): ")
                quantity = input("New quantity (leave blank to skip): ")
                fields = {}
                if price:
                    fields["price"] = float(price)
                if quantity:
                    fields["quantity"] = int(quantity)
                result = update_item(item_id, **fields)
                print(result if result else "Item not found.")

            elif choice == "6":
                item_id = int(input("Item ID to delete: "))
                deleted = delete_item(item_id)
                print("Deleted." if deleted else "Item not found.")

            elif choice == "7":
                name = input("Product name to search: ")
                results = find_on_api(name=name)
                print(results if results else "No results.")

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid option, try again.")

        except requests.exceptions.ConnectionError:
            print("Could not reach the API. Is the Flask server running (python run.py)?")
        except (ValueError, requests.exceptions.HTTPError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    run()