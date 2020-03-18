from .test_entities import AbstractTestEntities
from ..models import ScheduledSubject, Plan
from ..algorithm import ImprovementHelper


class TestImprovementHelper(AbstractTestEntities):
    """
    Tests for all static methods from ImprovementHelper
    """
    def setUp(self):
        super().setUp()

    def test_check_that_plans_are_correctly(self):
        plans = Plan.objects.all()
        for plan in plans:
            scheduled_subjects = ScheduledSubject.objects.filter(plan=plan)
            one_subject = scheduled_subjects[0]
            self.assertTrue(ImprovementHelper.check_subject_to_subject_time_exclude(one_subject, scheduled_subjects))

    def test_check_subject_to_subject_time_exclude_return_true(self):
        plan = Plan.objects.all()[0]
        scheduled_subjects = ScheduledSubject.objects.filter(plan=plan)
        value = ImprovementHelper.check_subject_to_subject_time_exclude(scheduled_subjects[0], scheduled_subjects)
        self.assertTrue(value)

    def test_check_subject_to_subject_time_return_false(self):
        plan = Plan.objects.all()[0]
        scheduled_subjects = ScheduledSubject.objects.filter(plan=plan)
        scheduled_subjects[1].whenStart = scheduled_subjects[0].whenStart
        scheduled_subjects[1].whenFinnish = scheduled_subjects[0].whenFinnish
        scheduled_subjects[1].dayOfWeek = scheduled_subjects[0].dayOfWeek
        value = ImprovementHelper.check_subject_to_subject_time(scheduled_subjects[0], scheduled_subjects)
        self.assertFalse(value)