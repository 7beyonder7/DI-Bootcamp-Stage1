from random import choice
from exercise import Dog


class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        dog_names = ", ".join([self.name] + [dog.name for dog in args])
        print(f"{dog_names} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = ["does a barrel roll", "stands on his back legs",
                      "shakes your hand", "plays dead"]
            print(f"{self.name} {choice(tricks)}")


if __name__ == "__main__":
    fido = PetDog("Fido", 2, 10)
    buddy = PetDog("Buddy", 3, 15)
    maxi = PetDog("Max", 4, 20)
    fido.train()
    fido.play(buddy, maxi)
    fido.do_a_trick()
