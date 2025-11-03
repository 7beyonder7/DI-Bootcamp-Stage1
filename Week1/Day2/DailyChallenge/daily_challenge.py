# Challenge 1: Multiples of a Number


# Key Python Topics:
# input() function
# Loops (for or while)
# Lists and appending items
# Basic arithmetic (multiplication)


# Instructions:
# 1. Ask the user for two inputs:

# A number (integer).
# A length (integer).
# 2. Create a program that generates a list of multiples of the given number.
# 3. The list should stop when it reaches the length specified by the user.


def get_int(prompt):
    while True:
        value = input(prompt)
        if value.lstrip('-').isdigit():
            return int(value)
        else:
            print("Invalid input. Please enter an integer.")


number = get_int("Enter a number: ")
length = get_int("Enter the desired length: ")

multiples = [number * i for i in range(1, length + 1)]

print("\nMultiples list:", multiples)

# Challenge 2: Remove Consecutive Duplicate Letters


# Key Python Topics:
# input() function
# Strings and string manipulation
# Loops (for or while)
# Conditional statements (if)


# Instructions:
# 1. Ask the user for a string.
# 2. Write a program that processes the string to remove consecutive duplicate letters.

# The new string should only contain unique consecutive letters.
# For example, “ppoeemm” should become “poem” (removes consecutive duplicates like ‘pp’, ‘ee’, and ‘mm’).
# 3. The program should print the modified string.

user_input_string = input('Please enter a string: ')
result = ''

for i, char in enumerate(user_input_string):
    is_not_last_el = i + 1 < len(user_input_string)
    next_char = user_input_string[i + 1] if is_not_last_el else None

    if char != next_char:
        result += char
print(result)
