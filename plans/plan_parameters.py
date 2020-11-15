
class ImprovementParameters:
    def __init__(self, tries, **kw):
        self.tries = tries
        super(ImprovementParameters, self).__init__(**kw)


class GeneticParameters:
    def __init__(self, number_of_generation, number_of_crossover, number_of_mutation, **kw):
        self.number_of_generation = number_of_generation
        self.number_of_crossover = number_of_crossover
        self.number_of_mutation = number_of_mutation
        super(GeneticParameters, self).__init__(**kw)


class AllParameters(ImprovementParameters, GeneticParameters):

    def __init__(self, number_of_generation, number_of_crossover, number_of_mutation):
        super(AllParameters, self).__init__(tries=number_of_generation,
                                            number_of_generation=number_of_generation,
                                            number_of_crossover=number_of_crossover,
                                            number_of_mutation=number_of_mutation)
