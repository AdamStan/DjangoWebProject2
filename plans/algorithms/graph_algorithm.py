# TODO: create plan with improvements!!!
import logging as logger
from entities.models import FieldOfStudy


class GraphAlgorithm:

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8, max_hour=19):
        pass

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        pass

    def save_the_best_result(self):
        logger.log(level=logger.INFO, msg="Algorithm not supported!")
