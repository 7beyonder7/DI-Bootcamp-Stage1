class Farm:
    def __init__(self, farm_name):
        self.farm = farm_name
        self.animals = {}
        # ... code to initialize name and animals attributes ...

    def add_animal(self, animal_type, count=1):
        # ... code to add or update animal count in animals dictionary ...
        self.animals[animal_type] = count
        print(self.animals)

    def get_info(self):
        pass
        # ... code to format animal info from animals dictionary ...

        # Test the code
macdonald = Farm("McDonald")
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)
# print(macdonald.get_info())
# output:
# McDonald's farm

# cow : 5
# sheep : 2
# goat : 12

#     E-I-E-I-0!
