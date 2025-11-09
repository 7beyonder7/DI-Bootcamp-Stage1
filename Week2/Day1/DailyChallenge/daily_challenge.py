class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type=None, count=1, **kwargs):
        if animal_type:  # single addition
            self.animals[animal_type] = self.animals.setdefault(
                animal_type, 0) + count
        for a, c in kwargs.items():  # multiple additions
            self.animals[a] = self.animals.setdefault(a, 0) + c

    def get_info(self):
        result = f"{self.name}'s farm\n\n"
        for animal, count in self.animals.items():
            result += f"{animal} : {count}\n"
        result += "\n    E-I-E-I-O!"
        return result

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_types = self.get_animal_types()
        animal_list = []
        for animal in animal_types:
            count = self.animals[animal]

            if count > 1:
                animal_list.append(animal + "s")
            else:
                animal_list.append(animal)

        if len(animal_list) > 1:
            animals_str = ", ".join(
                animal_list[:-1]) + " and " + animal_list[-1]
        else:
            animals_str = animal_list[0]

        return f"{self.name}'s farm has {animals_str}."


macdonald = Farm("McDonald")
macdonald.add_animal(cow=5, sheep=2, goat=12)
macdonald.add_animal("cow", 3)
print(macdonald.get_info())
print(macdonald.get_animal_types())
print(macdonald.get_short_info())
