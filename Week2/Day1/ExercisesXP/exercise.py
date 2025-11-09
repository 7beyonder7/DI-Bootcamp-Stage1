# 🌟 Exercise 1: Cats
# Key Python Topics:

# Classes and objects
# Object instantiation
# Attributes
# Functions


# Instructions:

# Use the provided Cat class to create three cat objects. Then, create a function to find the oldest cat and print its details.


# Step 1: Create Cat Objects

# Use the Cat class to create three cat objects with different names and ages.


# Step 2: Create a Function to Find the Oldest Cat

# Create a function that takes the three cat objects as input.
# Inside the function, compare the ages of the cats to find the oldest one.
# Return the oldest cat object.


# Step 3: Print the Oldest Cat’s Details

# Call the function to get the oldest cat.
# Print a formatted string: “The oldest cat is <cat_name>, and is <cat_age> years old.”
# Replace <cat_name> and <cat_age> with the oldest cat’s name and age.


class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age


tom_cat = Cat('Tom', 6)
barsik_cat = Cat('Barsik', 3)
oliver_cat = Cat('Oliver', 8)


def find_oldest_cat(*cats):
    oldest_cat = cats[0]
    for cat in cats:
        if cat.age > oldest_cat.age:
            oldest_cat = cat
    return oldest_cat


def find_oldest_cat(*cats):
    oldest = cats[0]
    for cat in cats:
        if cat.age > oldest.age:
            oldest = cat
    return oldest


oldest_cat = find_oldest_cat(tom_cat, barsik_cat, oliver_cat)
print(
    f"The oldest cat is {oldest_cat.name}, who is {oldest_cat.age} years old.")


# 🌟 Exercise 2 : Dogs
# Goal: Create a Dog class, instantiate objects, call methods, and compare dog sizes.


# Key Python Topics:

# Classes and objects
# Object instantiation
# Methods
# Attributes
# Conditional statements (if)


# Instructions:

# Create a Dog class with methods for barking and jumping. Instantiate dog objects, call their methods, and compare their sizes.


# Step 1: Create the Dog Class

# Create a class called Dog.
# In the __init__ method, take name and height as parameters and create corresponding attributes.
# Create a bark() method that prints “<dog_name> goes woof!”.
# Create a jump() method that prints “<dog_name> jumps <x> cm high!”, where x is height * 2.


# Step 2: Create Dog Objects

# Create davids_dog and sarahs_dog objects with their respective names and heights.


# Step 3: Print Dog Details and Call Methods

# Print the name and height of each dog.
# Call the bark() and jump() methods for each dog.


# Step 4: Compare Dog Sizes

class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")


my_dog = Dog('Mark', 50)
my_dog.bark()
my_dog.jump()

davids_dog = Dog('Bonnie', 45)
sarahs_dog = Dog('Clyde', 60)

print(f"{davids_dog.name} is {davids_dog.height} cm tall.")
davids_dog.bark()
davids_dog.jump()

print(f"{sarahs_dog.name} is {sarahs_dog.height} cm tall.")
sarahs_dog.bark()
sarahs_dog.jump()

if davids_dog.height > sarahs_dog.height:
    print(f"{davids_dog.name} is bigger than {sarahs_dog.name}.")
elif davids_dog.height < sarahs_dog.height:
    print(f"{sarahs_dog.name} is bigger than {davids_dog.name}.")
else:
    print(f"{davids_dog.name} and {sarahs_dog.name} are the same size!")


# Exercise 3 : Who’s the song producer?
# Goal: Create a Song class to represent song lyrics and print them.


# Key Python Topics:

# Classes and objects
# Object instantiation
# Methods
# Lists


# Instructions:

# Create a Song class with a method to print song lyrics line by line.


# Step 1: Create the Song Class

# Create a class called Song.
# In the __init__ method, take lyrics (a list) as a parameter and create a corresponding attribute.
# Create a sing_me_a_song() method that prints each element of the lyrics list on a new line.


# Example:

# stairway = Song(["There’s a lady who's sure", "all that glitters is gold", "and she’s buying a stairway to heaven"])

# stairway.sing_me_a_song()

# Output: There’s a lady who’s sureall that glitters is goldand she’s buying a stairway to heaven


class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)


enjoy_the_silence = Song([
    "Words like violence",
    "Break the silence",
    "Come crashing in",
    "Into my little world",
    "Painful to me",
    "Pierce right through me",
    "Can't you understand",
    "Oh my little girl"
])

enjoy_the_silence.sing_me_a_song()
