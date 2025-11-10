from random import randint, choice, random


class Gene:
    def __init__(self, value=randint(0, 1)):
        if value not in [0, 1]:
            raise ValueError("Gene: value must be 0 or 1")
        self.value = value

    def flip(self):
        self.value = 1 - self.value


class Chromosome:
    def __init__(self, genes):
        self.genes = genes

    def flip(self):
        if choice([True, False]) == False:
            for i in range(len(self.genes)):
                self.genes[i].flip()

    def get_genes(self):
        lst = []
        for gene in self.genes:
            lst.append(gene.value)
        return lst


class DNA:
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes

    def flip(self):
        if choice([True, False]) == True:
            for i in range(len(self.chromosomes)):
                self.chromosomes[i].flip()

    def get_chromosomes(self):
        chroms = []
        for chrom in self.chromosomes:
            lst = chrom.get_genes()
            chroms.append(lst)
        return chroms


class Organism:
    def __init__(self, dna, environment):
        self.dna = dna
        self.environment = environment

    def mutate(self):
        if (random() < self.environment):
            self.dna.flip()

    def check_all_ones(self):
        dna_list = self.dna.get_chromosomes()
        for lst in dna_list:
            for g in lst:
                if g == 0:
                    return False
        return True


my_dna = DNA([Chromosome([Gene() for _ in range(10)]) for _ in range(10)])
main_org = Organism(my_dna, environment=0.5)
generations = 0
while True:
    main_org.mutate()
    generations += 1
    if main_org.check_all_ones() is True:
        break

print(f"it took {generations} generations to finish")
