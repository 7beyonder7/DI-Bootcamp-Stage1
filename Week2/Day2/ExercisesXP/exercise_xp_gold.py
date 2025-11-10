# Exercise 1: Bank Account
# Instructions
# Part I:

# Create a class called BankAccount that contains the following attributes and methods:
# balance - (an attribute)
# __init__ : initialize the attribute
# deposit : - (a method) accepts a positive int and adds to the balance, raise an Exception if the int is not positive.
# withdraw : - (a method) accepts a positive int and deducts from the balance, raise an Exception if not positive


# Part II : Minimum balance account

# Create a MinimumBalanceAccount that inherits from BankAccount.
# Extend the __init__ method and accept a parameter called minimum_balance with a default value of 0.
# Override the withdraw method so it only allows the user to withdraw money if the balance remains higher than the minimum_balance, raise an Exception if not.


# Part III: Expand the bank account class

# Add the following attributes to the BankAccount class:
# username
# password
# authenticated (False by default)

# Create a method called authenticate. This method should accept 2 strings : a username and a password. If the username and password match the attributes username and password the method should set the authenticated boolean to True.

# Edit withdraw and deposit to only work if authenticated is set to True, if someone tries an action without being authenticated raise an Exception


# Part IV: BONUS Create an ATM class

# __init__:
# Accepts the following parameters: account_list and try_limit.

# Validates that account_list contains a list of BankAccount or MinimumBalanceAccount instances.
# Hint: isinstance()

# Validates that try_limit is a positive number, if you get an invalid input raise an Exception, then move along and set try_limit to 2.
# Hint: Check out this tutorial

# Sets attribute current_tries = 0

# Call the method show_main_menu (see below)

# Methods:
# show_main_menu:
# This method will start a while loop to display a menu letting a user select:
# Log in : Will ask for the users username and password and call the log_in method with the username and password (see below).
# Exit.

# log_in:
# Accepts a username and a password.

# Checks the username and the password against all accounts in account_list.
# If there is a match (ie. use the authenticate method), call the method show_account_menu.
# If there is no match with any existing accounts, increment the current tries by 1. Continue asking the user for a username and a password, until the limit is reached (ie. try_limit attribute). Once reached display a message saying they reached max tries and shutdown the program.

# show_account_menu:
# Accepts an instance of BankAccount or MinimumBalanceAccount.
# The method will start a loop giving the user the option to deposit, withdraw or exit.

import sys


class BankAccount:
    def __init__(self, balance=0, username="", password=""):
        self.balance = balance
        self.username = username
        self.password = password
        self.authenticated = False

    def authenticate(self, username: str, password: str) -> bool:
        if self.username == username and self.password == password:
            self.authenticated = True
            return True
        return False

    def _ensure_authenticated(self):
        if not self.authenticated:
            raise PermissionError(
                "Action not allowed: user not authenticated.")

    def deposit(self, amount: int):
        self._ensure_authenticated()
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Deposit amount must be a positive integer.")
        self.balance += amount
        print(f"Deposited {amount}. Balance: {self.balance}")

    def withdraw(self, amount: int):
        self._ensure_authenticated()
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive integer.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        print(f"Withdrew {amount}. Balance: {self.balance}")


class MinimumBalanceAccount(BankAccount):
    def __init__(self, balance=0, username="", password="", minimum_balance=0):
        super().__init__(balance, username, password)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount: int):
        self._ensure_authenticated()
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive integer.")
        if self.balance - amount < self.minimum_balance:
            raise ValueError(
                f"Cannot withdraw {amount}: balance would drop below minimum ({self.minimum_balance})."
            )
        self.balance -= amount
        print(f"Withdrew {amount}. Balance: {self.balance}")


class ATM:
    def __init__(self, account_list, try_limit=3):
        if not isinstance(account_list, list):
            raise TypeError(
                "account_list must be a list of BankAccount/MinimumBalanceAccount instances.")
        for acc in account_list:
            if not isinstance(acc, (BankAccount, MinimumBalanceAccount)):
                raise TypeError(
                    f"Invalid item {acc!r}: all items must be BankAccount or MinimumBalanceAccount."
                )
        self.account_list = account_list

        self.current_tries = 0
        try:
            if not isinstance(try_limit, int) or try_limit <= 0:
                raise ValueError("try_limit must be a positive integer.")
            self.try_limit = try_limit
        except Exception as e:
            print(f"[ATM WARNING] {e}. Falling back to try_limit=2.")
            self.try_limit = 2

        self.show_main_menu()

    def show_main_menu(self):
        while True:
            print("\n=== ATM Main Menu ===")
            print("1) Log in")
            print("2) Exit")
            choice = input("Select an option: ").strip()
            if choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                self.log_in(username, password)
            elif choice == "2":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid selection. Please try again.")

    def log_in(self, username: str, password: str):
        while True:
            for acc in self.account_list:
                if acc.authenticate(username, password):
                    print(f"Welcome, {acc.username}!")
                    self.current_tries = 0
                    self.show_account_menu(acc)
                    return

            self.current_tries += 1
            if self.current_tries >= self.try_limit:
                print("You have reached the maximum number of tries. Shutting down.")
                sys.exit(1)
            else:
                print(
                    f"Login failed. Tries: {self.current_tries}/{self.try_limit}")
                username = input("Username: ").strip()
                password = input("Password: ").strip()

    def show_account_menu(self, account: BankAccount):
        while True:
            print("\n=== Account Menu ===")
            print("1) Balance")
            print("2) Deposit")
            print("3) Withdraw")
            print("4) Log out")
            choice = input("Select an option: ").strip()

            if choice == "1":
                print(f"Current balance: {account.balance}")

            elif choice == "2":
                deposit_amount = input("Amount to deposit (integer): ").strip()
                try:
                    account.deposit(int(deposit_amount))
                except Exception as e:
                    print(f"Error: {e}")

            elif choice == "3":
                withdraw_amount = input(
                    "Amount to withdraw (integer): ").strip()
                try:
                    account.withdraw(int(withdraw_amount))
                except Exception as e:
                    print(f"Error: {e}")

            elif choice == "4":
                account.authenticated = False
                print("Logged out.")
                break
            else:
                print("Invalid selection. Please try again.")


if __name__ == "__main__":
    a1 = BankAccount(balance=300, username="alice", password="1234")
    a2 = MinimumBalanceAccount(
        balance=1000, username="bob", password="abcd", minimum_balance=200)
    ATM([a1, a2], try_limit=3)
