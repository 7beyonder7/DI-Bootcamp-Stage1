menu = {
    "espresso": 7.0,
    "latte": 12.0,
    "cappuccino": 10.0
}


def show_menu(menu_dict):
    if not menu_dict:
        print("The menu is empty.")
        return
    print("Current menu:")
    for drink, price in menu_dict.items():
        print(f"{drink} - {price:.1f}₪")


def get_valid_price(prompt="Enter price: "):
    while True:
        value = input(prompt).strip()
        try:
            price = float(value)
            if price < 0:
                print("Invalid price.")
                continue
            return price
        except ValueError:
            print("Invalid price. Try again.")


def get_valid_percent(prompt="Enter discount percent (0-100): "):
    while True:
        value = input(prompt).strip()
        try:
            p = float(value)
            if 0 <= p <= 100:
                return p
            print("Percent must be between 0 and 100.")
        except ValueError:
            print("Invalid percent. Try again.")


def add_item(menu_dict):
    name = input("Enter new drink name: ").strip().lower()
    if not name:
        print("Item name cannot be empty.")
        return
    if name in menu_dict:
        print("Item already exists!")
        return
    price = get_valid_price("Enter price: ")
    menu_dict[name] = price
    print(f"\"{name}\" added!")


def update_price(menu_dict):
    name = input("Which drink do you want to update? ").strip().lower()
    if name in menu_dict:
        new_price = get_valid_price("Enter the new price: ")
        menu_dict[name] = new_price
        print("Price updated!")
    else:
        print("Item not found.")


def delete_item(menu_dict):
    name = input("Which drink do you want to delete? ").strip().lower()
    if name in menu_dict:
        del menu_dict[name]
        print("Item deleted.")
    else:
        print("Item not found.")


def search_item(menu_dict):
    name = input("Enter drink name to search: ").strip().lower()
    if name in menu_dict:
        print(f"{name} - {menu_dict[name]:.1f}₪")
    else:
        print("Not in the menu.")


def apply_discount(menu_dict, percent):
    for drink in menu_dict:
        menu_dict[drink] = round(menu_dict[drink] * (1 - percent / 100), 2)
    print(f"Applied {percent:.0f}% discount to all items.")


def show_options():
    print("What would you like to do?")
    print("1. Show menu")
    print("2. Add item")
    print("3. Update price")
    print("4. Delete item")
    print("5. Exit")
    print("6. Search item")
    print("7. Apply discount")


def run_coffee_shop():
    while True:
        show_options()
        choice = input("> ").strip()

        if choice == "1":
            show_menu(menu)
        elif choice == "2":
            add_item(menu)
        elif choice == "3":
            update_price(menu)
        elif choice == "4":
            delete_item(menu)
        elif choice == "5":
            print("Goodbye!")
            break
        elif choice == "6":
            search_item(menu)
        elif choice == "7":
            percent = get_valid_percent()
            apply_discount(menu, percent)
        else:
            print("Invalid choice, try again.")


run_coffee_shop()
