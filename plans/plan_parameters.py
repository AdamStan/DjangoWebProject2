
class PlanParameters:
    def __init__(self, min_hour, max_hour, semester_type, how_many_groups):
        self.min_hour = min_hour
        self.max_hour = max_hour
        self.semester_type = semester_type
        self.how_many_groups = how_many_groups


class ImprovementParameters:
    def __init__(self, tries):
        self.tries = tries


class GeneticParameters:
    def __init__(self, number_of_generation, number_of_crossover, number_of_mutation):
        self.number_of_generation = number_of_generation
        self.number_of_crossover = number_of_crossover
        self.number_of_mutation = number_of_mutation
