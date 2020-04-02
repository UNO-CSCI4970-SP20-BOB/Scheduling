import unittest
from Scheduling_Example import *
from unittest.mock import Mock


class MyTestCase(unittest.TestCase):

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    shifts = ['morning', 'evening', 'night']
    days_shifts = {day: shifts for day in days}
    workers = ['W' + str(i) for i in range(1, 11)]
    model = ConcreteModel()
    model.works = Var(((worker, day, shift) for worker in workers
                       for day in days
                       for shift in days_shifts[day]),
                      within=Binary, initialize=0)
    model.needed = Var(workers, within=Binary, initialize=0)
    model.no_pref = Var(workers, within=Binary, initialize=0)

    def test_get_workers_needed(self):
        needed = model.needed
        result = get_workers_needed(needed)

        self.assertEqual(result, ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W10'])

    def test_get_work_table(self):
        expected = {'Fri': {'evening': ['W2', 'W4'], 'morning': ['W1', 'W3'], 'night': ['W10']},
                    'Mon': {'evening': ['W2', 'W4'], 'morning': ['W5', 'W10'], 'night': ['W3']},
                    'Sat': {'evening': ['W1', 'W3'], 'morning': ['W5', 'W6'], 'night': ['W2']},
                    'Sun': {'evening': ['W6'], 'morning': ['W5'], 'night': ['W3']},
                    'Thu': {'evening': ['W2', 'W10'], 'morning': ['W1', 'W4'], 'night': ['W6']},
                    'Tue': {'evening': ['W4', 'W10'], 'morning': ['W1', 'W6'], 'night': ['W3']},
                    'Wed': {'evening': ['W2', 'W10'], 'morning': ['W1', 'W6'], 'night': ['W5']}}
        works = model.works
        result = get_work_table(works)
        self.assertEqual(result, expected)

    def test_get_no_preference(self):
        pref = model.no_pref
        result = get_no_preference(pref)
        self.assertEqual(result, ['W1', 'W2'])


if __name__ == '__main__':
    unittest.main()
