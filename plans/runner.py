from plans.algorithms import RandomPlanAlgorithm, ImprovementAlgorithm, GeneticAlgorithm, NNPlanGeneratorAlgorithm, \
    GraphAlgorithm


def run_it_in_shell():
    cpm = RandomPlanAlgorithm()
    cpm.create_plan_async_without_deleting()
    cpm.save_the_best_result()


def provide_creator(algorithm_name):
    if algorithm_name == "algorithm-random":
        return RandomPlanAlgorithm()
    if algorithm_name == "algorithm-with-improvement":
        return ImprovementAlgorithm()
    if algorithm_name == "algorithm-genetic":
        return GeneticAlgorithm()
    if algorithm_name == "algorithm-nn":
        return NNPlanGeneratorAlgorithm()
    if algorithm_name == "algorithm-graph":
        return GraphAlgorithm()
