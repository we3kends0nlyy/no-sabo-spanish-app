import unittest
from project4 import ask_for_inputs
from project4 import main
from project4 import Option
from project4 import Rule
from project4 import Grammar
import tempfile
from pathlib import Path
from unittest.mock import patch

def test_file():
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as input_file:
        input_file.write('{\n')
        input_file.write('HowIsBoo\n')
        input_file.write('1 Boo is [Adjective] today\n')
        input_file.write('}\n')
        input_file.write('\n')
        input_file.write('{\n')
        input_file.write('Adjective\n')
        input_file.write('100 perfect\n')
        input_file.write('}\n')
    return input_file
class TestRandomNum(unittest.TestCase):
    def test_random_num_choose(self):
        rule = Rule()
        self.assertEqual(rule.generate_random_number([['HowIsBoo'], ['100', 'Boo', 'is', '[Adjective]', 'today', 'and', '[Verb]']]), ['100', 'Boo', 'is', '[Adjective]', 'today', 'and', '[Verb]'])

class TestGrammar(unittest.TestCase):
    def test_grammar_gen_sentence_frag(self):
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        file_1.close()

class TestInputs(unittest.TestCase):
    input_file = test_file()
    @patch('builtins.input', side_effect=[Path(input_file.name), 1, "HowIsBoo"])
    def test_ask_for_input(self, _):
        result = main(True)
        self.assertEqual(result, None)

class TestGramGenSenFrag(unittest.TestCase):
    def test_gram_gen_sent_frag(self):
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        x = grammar.generate_sentence_fragment("empty", "HowIsBoo", grammar, True)
        try:
            next(x)
        except StopIteration:
            pass
        file_1.close()

class TestRuleGenSenFrag(unittest.TestCase):
    def test_rule_gen_sent_frag(self):
        rule = Rule()
        x = rule.generate_sentence_fragment([['HowIsBoo'], ['1', 'Boo', 'is', '[Adjective]', 'today', 'and', '[Verb]']], "HowIsBoo", "grammar", True)
        try:
            next(x)
        except StopIteration:
            pass

class TestOptionGenSenFrag(unittest.TestCase):
    def test_option_gen_sent_frag(self):
        option = Option()
        y = option.generate_sentence_fragment(['[Adjective]'], "HowIsBoo", "grammar", True)
        try:
            next(y)
        except StopIteration:
            pass

if __name__ == "__main__":
    unittest.main()