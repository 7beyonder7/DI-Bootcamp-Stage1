import random


class Gene():
    def __init__(self, value=random.randint(0, 1)):
        if value not in [0, 1]:
            raise ValueError("Gene: value must be 0 or 1")
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"

    def flip(self):
        self.value = 1 - self.value

    def get_value(self):
        return self.value


class Chromosome():
    def __init__(self, genes):
        try:
            assert (type(genes) == list and len(genes) == 10)
            for gene in genes:
                assert isinstance(gene, Gene)
        except AssertionError as e:
            raise ValueError("Chromosome: genes must be a list of 10 Genes")
        else:
            self.genes = genes

    def flip(self):
        for i in range(len(self.genes)):
            if random.choice([False, True]) is True:
                self.genes[i].flip()

    def __str__(self):
        return "".join(self.genes)

    def __repr__(self):
        return "".join(self.genes)

    def get_genes(self):
        lst = []
        for gene in self.genes:
            lst.append(gene.value)
        return lst


class DNA():
    def __init__(self, chromosomes):
        try:
            assert (type(chromosomes) == list and len(chromosomes) == 10)
            for chrom in chromosomes:
                assert isinstance(chrom, Chromosome)
        except AssertionError as e:
            raise ValueError(
                "DNA: chromosomes must be a list of 10 Chromosomes")
        else:
            self.chromosomes = chromosomes

    def flip(self):
        for i in range(len(self.chromosomes)):
            if random.choice([False, True]) is True:
                self.chromosomes[i].flip()

    def get_chromosomes(self):
        chroms = []
        for chrom in self.chromosomes:
            lst = chrom.get_genes()
            chroms.append(lst)
        return chroms


class Organism():
    def __init__(self, dna: DNA, environment: float):
        try:
            assert (type(dna) == DNA)
        except AssertionError as e:
            raise ValueError("Organism: dna must be an instance of DNA")
        else:
            self.dna = dna
            self.environment = environment

    def mutate(self):
        if (random.random() > self.environment):
            self.dna.flip()

    def check_all_ones(self):
        dna_list = self.dna.get_chromosomes()
        for lst in dna_list:
            for g in lst:
                if g == 0:
                    return False
        return True


main_dna = DNA([Chromosome([Gene() for _ in range(10)]) for _ in range(10)])
main_org = Organism(main_dna, environment=0.5)
generations = 0
while True:
    main_org.mutate()
    generations += 1
    if main_org.check_all_ones() is True:
        break

print(f"it took {generations} generations to finish")
