
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


class NeuralNetworkParameters:
    def __init__(self, type_of_neural_network, **kw):
        self.type_of_neural_network = type_of_neural_network
        super(NeuralNetworkParameters, self).__init__(**kw)


class AllParameters(ImprovementParameters, GeneticParameters, NeuralNetworkParameters):

    def __init__(self, number_of_generation, number_of_crossover, number_of_mutation, type_of_neural_network):
        super(AllParameters, self).__init__(tries=number_of_generation,
                                            number_of_generation=number_of_generation,
                                            number_of_crossover=number_of_crossover,
                                            number_of_mutation=number_of_mutation,
                                            type_of_neural_network=type_of_neural_network)
