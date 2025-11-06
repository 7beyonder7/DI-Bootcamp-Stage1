# Exercise 1: Converting Lists into Dictionaries
# Key Python Topics:

# Creating dictionaries
# Zip function or dictionary comprehension


# Instructions
# You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]
result = {key: value for key, value in zip(keys, values)}
print(result)

# Exercise 2: Cinemax #2
# Key Python Topics:

# Looping through dictionaries
# Conditionals
# Calculations


# Instructions
# Write a program that calculates the total cost of movie tickets for a family based on their ages.

# Family members’ ages are stored in a dictionary.
# The ticket pricing rules are as follows:
# Under 3 years old: Free
# 3 to 12 years old: $10
# Over 12 years old: $15


# Family Data:

# family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}


# Loop through the family dictionary to calculate the total cost.
# Print the ticket price for each family member.
# Print the total cost at the end.

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}


def calculate_tickets_cost(people_group):
    if not isinstance(people_group, dict) or not people_group:
        print("Invalid input. Expected a non-empty dictionary.")
        return
    total_cost = 0
    for name, age in people_group.items():
        if age < 3:
            price = 0
        elif 3 <= age <= 12:
            price = 10
        else:
            price = 15
        print(f"{name.capitalize()}’s ticket price: ${price}")
        total_cost += price

    print(f"\nTotal cost for tickets: ${total_cost}")


calculate_tickets_cost(family)

# Bonus:
# Allow the user to input family members’ names and ages, then calculate the total ticket cost.
peoples_group = {}

while True:
    name = input("Enter family member's name (or 'done' to finish): ").strip()
    if name.lower() == 'done':
        break
    if not name.isalpha():
        print("Invalid name. Please use only letters.\n")
        continue

    while True:
        age_input = input(f"Enter {name}'s age: ").strip()
        if not age_input.isdigit():
            print("Invalid age. Please enter a positive number.\n")
            continue
        age = int(age_input)
        break

    peoples_group[name] = age

calculate_tickets_cost(peoples_group)

# Exercise 3: Zara
# Key Python Topics:

# Creating dictionaries
# Accessing and modifying dictionary elements
# Dictionary methods like .pop() and .update()


# Instructions
# Create and manipulate a dictionary that contains information about the Zara brand.


# Brand Information:

# name: Zara
# creation_date: 1975
# creator_name: Amancio Ortega Gaona
# type_of_clothes: men, women, children, home
# international_competitors: Gap, H&M, Benetton
# number_stores: 7000
# major_color:
#    France: blue,
#    Spain: red,
#    US: pink, green


# Create a dictionary called brand with the provided data.
# Modify and access the dictionary as follows:
# Change the value of number_stores to 2.
# Print a sentence describing Zara’s clients using the type_of_clothes key.
# Add a new key country_creation with the value Spain.
# Check if international_competitors exists and, if so, add “Desigual” to the list.
# Delete the creation_date key.
# Print the last item in international_competitors.
# Print the major colors in the US.
# Print the number of keys in the dictionary.
# Print all keys of the dictionary.

brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": "blue",
        "Spain": "red",
        "US": ["pink", "green"]
    }
}

brand["number_stores"] = 2

types = ", ".join(brand["type_of_clothes"])
print(f"Zara sells products for those who shop for: {types}.")

brand["country_creation"] = "Spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")

if "creation_date" in brand:
    del brand["creation_date"]


last_competitor = brand["international_competitors"][-1] if brand.get(
    "international_competitors") else None
print("Last international competitor:", last_competitor)

us_colors = brand["major_color"]["US"]
print("Major colors in the US: ", ", ".join(us_colors)
      if isinstance(us_colors, list) else us_colors)

print("Number of keys in brand: ", len(brand))

print("All keys: ", list(brand.keys()))

# Bonus:

# Create another dictionary called more_on_zara with creation_date and number_stores. Merge this dictionary with the original brand dictionary and print the result.

more_on_zara = {
    "creation_date": 2025,
    "number_stores": 77
}

merged_zara = {**brand, ** more_on_zara}
print(merged_zara)

# Exercise 4: Disney Characters
# Key Python Topics:

# Looping with indexes
# Dictionary creation
# Sorting


# Instructions
# You are given a list of Disney characters. Create three dictionaries based on different patterns as shown below:


# Character List:

# users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]


# Expected Results:

# 1. Create a dictionary that maps characters to their indices:

# {"Mickey": 0, "Minnie": 1, "Donald": 2, "Ariel": 3, "Pluto": 4}


# 2. Create a dictionary that maps indices to characters:

# {0: "Mickey", 1: "Minnie", 2: "Donald", 3: "Ariel", 4: "Pluto"}


# 3. Create a dictionary where characters are sorted alphabetically and mapped to their indices:

# {"Ariel": 0, "Donald": 1, "Mickey": 2, "Minnie": 3, "Pluto": 4}

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

char_to_index = {item: index for index, item in enumerate(users)}
print(char_to_index)

index_to_char = {index: item for index, item in enumerate(users)}
print(index_to_char)

char_to_index_sorted = {item: index for index,
                        item in enumerate(sorted(users))}
print(char_to_index_sorted)
