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
