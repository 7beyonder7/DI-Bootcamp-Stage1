# Exercise 1: Currencies
# Goal: Implement dunder methods for a Currency class to handle string representation,
# integer conversion, addition, and in -place addition.


# Key Python Topics:

# Dunder methods(__str__, __repr__, __int__, __add__, __iadd__)
# Type checking(isinstance())
# Raising exceptions(raise TypeError)


import random
import string
import datetime
from faker import Faker


class Currency:
    __slots__ = ("currency", "amount")

    def __init__(self, currency: str, amount: int | float):
        if not isinstance(currency, str):
            raise TypeError("currency must be str")
        if not isinstance(amount, (int, float)):
            raise TypeError("amount must be int or float")
        self.currency = currency
        self.amount = amount

    def __str__(self) -> str:
        suffix = "" if self.amount == 1 or self.currency.endswith("s") else "s"
        return f"{self.amount} {self.currency}{suffix}"

    def __repr__(self) -> str:
        return f"'{str(self)}'"

    def __int__(self) -> int:
        return int(self.amount)

    def _ensure_same_currency(self, other: "Currency") -> None:
        if self.currency != other.currency:
            raise TypeError(
                f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
            )

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.amount + other
        if isinstance(other, Currency):
            self._ensure_same_currency(other)
            return self.amount + other.amount
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return other + self.amount
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Currency):
            self._ensure_same_currency(other)
            self.amount += other.amount
            return self
        if isinstance(other, (int, float)):
            self.amount += other
            return self
        return NotImplemented


c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

# the comment is the expected output
print(c1)  # '5 dollars'
print(int(c1))  # 5
print(repr(c1))  # '5 dollars'
print(c1 + 5)  # 10
print(c1 + c2)  # 15
print(c1)  # 5 dollars
c1 += 5
print(c1)  # 10 dollars
c1 += c2
print(c1)  # 20 dollars
try:
    print(c1 + c3)
except TypeError as e:  # TypeError: Cannot add between Currency type <dollar> and <shekel>
    print(e)

# Exercise 3: String module
# Goal: Generate a random string of length 5 using the string module.


# Instructions:

# Use the string module to generate a random string of length 5, consisting of uppercase and lowercase letters only.


# Key Python Topics:

# string module
# random module
# String concatenation


# Step 1: Import the string and random modules

# Import the string and random modules.


# Step 2: Create a string of all letters

# Read about the strings methods HERE to find the best methods for this step


# Step 3: Generate a random string

# Use a loop to select 5 random characters from the combined string.
# Concatenate the characters to form the random string.
letters = string.ascii_letters
random_string = ''

for i in range(5):
    random_char = random.choice(letters)
    random_string += random_char
print("Random string:", random_string)

# Exercise 4: Current Date
# Goal: Create a function that displays the current date.


# Key Python Topics:

# datetime module


# Instructions:

# Use the datetime module to create a function that displays the current date.

# Step 1: Import the datetime module

# Step 2: Get the current date

# Step 3: Display the date
def display_current_date():
    current_date = datetime.date.today()
    print("Today's date is:", current_date)


display_current_date()


# Exercise 5: Amount of time left until January 1st
# Goal: Create a function that displays the amount of time left until January 1st.


# Key Python Topics:

# datetime module
# Time difference calculations


# Instructions:

# Use the datetime module to calculate and display the time left until January 1st.
# more info about this module HERE

# Step 1: Import the datetime module

# Step 2: Get the current date and time

# Step 3: Create a datetime object for January 1st of the next year

# Step 4: Calculate the time difference

# Step 5: Display the time difference

def time_until_new_year():
    now = datetime.datetime.now()
    next_year = now.year + 1
    new_year_day = datetime.datetime(next_year, 1, 1)
    time_left = new_year_day - now

    print(f"Time left until January 1st: {time_left}")


time_until_new_year()

# Exercise 6: Birthday and minutes
# Key Python Topics:

# datetime module
# datetime.datetime.strptime() (parsing dates)
# Time difference calculations
# .total_seconds() method


# Instructions:

# Create a function that accepts a birthdate as an argument (in the format of your choice),
# then displays a message stating how many minutes the user lived in his life.

def minutes_lived(birthdate_str):
    birthdate = datetime.datetime.strptime(birthdate_str, "%d/%m/%Y")
    now = datetime.datetime.now()
    difference = now - birthdate
    minutes = difference.total_seconds() / 60
    print(f"You have lived approximately {int(minutes):,} minutes so far!")


minutes_lived("31/12/1991")

# Exercise 7: Faker Module
# Goal: Use the faker module to generate fake user data and store it in a list of dictionaries.
# Read more about this module HERE


# Key Python Topics:

# faker module
# Dictionaries
# Lists
# Loops


# Instructions:

# Install the faker module and use it to create a list of dictionaries,
# where each dictionary represents a user with fake data.

# Step 1: Install the faker module

# Step 2: Import the faker module

# Step 3: Create an empty list of users

# Step 4: Create a function to add users

# Create a function that takes the number of users to generate as an argument.
# Inside the function, use a loop to generate the specified number of users.
# For each user, create a dictionary with the keys name, address, and language_code.
# Use the faker instance to generate fake data for each key:
# name: faker.name()
# address: faker.address()
# language_code: faker.language_code()
# Append the user dictionary to the users list.
# Step 5: Call the function and print the users list

faker = Faker()
users = []


def generate_users(n):
    for _ in range(n):
        user = {
            "name": faker.name(),
            "address": faker.address(),
            "language_code": faker.language_code()
        }
        users.append(user)


generate_users(5)
for i, user in enumerate(users, start=1):
    print(f"User {i}:")
    print(f"  name: {user['name']}")
    formatted_address = "\n    ".join(user['address'].split("\n"))
    print(f"  address: {formatted_address}")
    print(f"  language_code: {user['language_code']}\n")
    print("-" * 40)
