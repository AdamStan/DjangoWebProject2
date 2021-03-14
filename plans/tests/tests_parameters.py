from plans.plan_parameters import AllParameters
import unittest


class TestAllParameters(unittest.TestCase):
    def test_all_parameter(self):
        parameters = AllParameters(number_of_crossover=0.2, number_of_mutation=0.5, number_of_generation=100,
                                   type_of_neural_network=1)
        self.assertEqual(parameters.tries, 100)
        self.assertEqual(parameters.number_of_generation, 100)
        self.assertEqual(parameters.number_of_mutation, 0.5)
        self.assertEqual(parameters.number_of_crossover, 0.2)
        self.assertEqual(parameters.type_of_neural_network, 1)


if __name__ == '__main__':
    unittest.main()
