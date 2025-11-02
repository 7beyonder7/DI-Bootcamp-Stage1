# Instructions:
# 1. Ask for User Input:

# The string must be exactly 10 characters long.
# 2. Check the Length of the String:

# If the string is less than 10 characters, print: "String not long enough."
# If the string is more than 10 characters, print: "String too long."
# If the string is exactly 10 characters, print: "Perfect string" and proceed to the next steps.
# 3. Print the First and Last Characters:

# Once the string is validated, print the first and last characters.
# 4. Build the String Character by Character:

# Using a for loop, construct and print the string character by character. Start with the first character, then the first two characters, and so on, until the entire string is printed.
# Hint: You can create a loop that goes through the string, adding one character at a time, and print it progressively.

from random import shuffle

user_input = input("The string must be exactly 10 characters long: ")

if len(user_input) < 10:
    print("String not long enough.")
elif len(user_input) > 10:
    print("String too long.")
else:
    print("Perfect string")

print(f"First character: {user_input[0]}")
print(f"Last character: {user_input[-1]}")

print("\nUsing a for loop to print each character:")
for i in range(0, len(user_input) + 1):
    print(user_input[:i])

print("\nShuffling string:")
user_input_char_list = list(user_input)
shuffle(user_input_char_list)
print("".join(user_input_char_list))
