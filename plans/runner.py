from plans.algorithms import RandomPlanAlgorithm, ImprovementAlgorithm, GeneticAlgorithmRunner, NNPlanGeneratorAlgorithm, \
    GraphAlgorithmRunner


def provide_creator(algorithm_name, plan_parameters):
    if algorithm_name == "algorithm-random":
        return RandomPlanAlgorithm()
    if algorithm_name == "algorithm-with-improvement":
        return ImprovementAlgorithm(tries=plan_parameters.tries)
    if algorithm_name == "algorithm-genetic":
        return GeneticAlgorithmRunner(plan_parameters.number_of_generation, plan_parameters.number_of_crossover,
                                      plan_parameters.number_of_mutation)
    if algorithm_name == "algorithm-nn":
        return NNPlanGeneratorAlgorithm()
    if algorithm_name == "algorithm-graph":
        return GraphAlgorithmRunner()
