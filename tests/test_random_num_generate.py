import unittest
from project4 import Rule

class TestRandomNum(unittest.TestCase):
    def test_random_num_choose(self):
        rule = Rule()
        self.assertEqual(rule.generate_random_number([['HowIsBoo'], ['100', 'Boo', 'is', '[Adjective]', 'today', 'and', '[Verb]']]), ['100', 'Boo', 'is', '[Adjective]', 'today', 'and', '[Verb]'])


if __name__ == "__main__":
    unittest.main()