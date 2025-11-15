
# 1. What is a class?
# A class is a blueprint or template for creating objects (e.g. instances of a class).
# It defines attributes and methods that the created objects/instances will have.

# 2. What is an instance?
# An instance is an individual object created from a class.
# It is the the real data object with attributes and methods (if exist) built using the class blueprint.

# 3. What is encapsulation?
# Encapsulation means bundling data and methods inside a class and restricting access to some of the internal details.
# It protects the object’s internal state from unintended interference.

# 4. What is abstraction?
# Abstraction means hiding complex internal logic and exposing only what is necessary.
# You interact with a simple interface, not the implementation e.g. you have no idea what happens under the hood.

# 5. What is inheritance?
# Inheritance is a mechanism that allows a class (child/subclass) to inherit attributes and methods from another class (parent/superclass).
# It promotes code reuse.

# 6. What is multiple inheritance?
# Multiple inheritance means a class can inherit from more than one parent class (e.g. nested pronciple).

# 7. What is polymorphism?
# Polymorphism means different classes can implement the same method name, but each behaves differently.

# 8. What is method resolution order (MRO)?
# MRO is the order in which Python looks for methods and attributes when multiple classes are involved.
# Python looks for method in the following order: the object’s own class, the class’s parent(s), Parent of the parent
# …and so on until it reaches object (the root of all classes)
# It determines which version of a method is used.


import random


class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self):
        self.cards = []
        self.shuffle()

    def shuffle(self):
        self.cards = [Card(suit, val)
                      for suit in self.suits for val in self.values]
        random.shuffle(self.cards)

    def __repr__(self):
        return f"{self.cards}"

    def deal(self):
        if not self.cards:
            raise ValueError("No cards left in the deck!")
        random_card = random.choice(self.cards)
        self.cards.remove(random_card)
        return random_card


deck = Deck()

print(len(deck.cards))  # 52

card1 = deck.deal()
print("You got:", card1)

print(len(deck.cards))  # 51

deck.shuffle()  # reset to full deck + shuffle again
print(len(deck.cards))  # 52
