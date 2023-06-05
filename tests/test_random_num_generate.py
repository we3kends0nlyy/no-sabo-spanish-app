import unittest
from project4 import main
from project4 import Option
from project4 import Rule
from project4 import Grammar
from project4 import VariableSymbol
from project4 import TerminalSymbol
from project4 import call_duck_typed_method
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO

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

class TestInputRandomNum(unittest.TestCase):
        input_file = test_file()
        @patch('builtins.input', side_effect=[Path(input_file.name), 1, "HowIsBoo"])
        def test_ask_for_input(self, _):
            result = StringIO()
            with patch('sys.stdout', new=result):
                main(True)
            output_print = result.getvalue().strip()
            self.assertEqual(output_print, "Boo is perfect today")

class TestGramGenSenFrag(unittest.TestCase):
    def test_gram_gen_sent_frag(self):
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        x = grammar.generate_sentence_fragment("Adjective", "HowIsBoo", "Adjective", grammar)
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

class TestVarGenSenFrag(unittest.TestCase):
    def test_var_gen_sen_frag(self):
        variable = VariableSymbol()
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        y = variable.generate_sentence_fragment(['[Adjective]', 'today', 'and', '[Verb]'], "hi", "Adjective", grammar, 0)
        try:
            next(y)
            next(y)
            file_1.close()
        except StopIteration:
            file_1.close()

class TestTermGenSenFrag(unittest.TestCase):
    def test_term_gen_sen_frag(self):
        terminal = TerminalSymbol()
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        self.assertEqual(terminal.generate_sentence_fragment(['today'], "hi", "Adjective", grammar, 0),"today")
        file_1.close()

    def test_term_gen_sen_frag2(self):
        terminal = TerminalSymbol()
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        self.assertEqual(terminal.generate_sentence_fragment([''], "hi", "Adjective", grammar, 0),"")
        file_1.close()

class TestOptionGenSenFrag(unittest.TestCase):
    def test_option_gen_sent_frag(self):
        option = Option()
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        y = option.generate_sentence_fragment(['[Adjective]', 'today', 'and', '[Verb]'], option, "Adjective", grammar)
        try:
            next(y)
            next(y)
            file_1.close()
        except StopIteration:
            file_1.close()

class TestDuckTypedMethod(unittest.TestCase):
    def test_duck_typed_method(self):
        option = Option()
        input_file = test_file()
        grammar = Grammar()
        file_1 = open(input_file.name, "r")
        grammar.store_rules(file_1)
        y = call_duck_typed_method(['[Adjective]', 'today', 'and', '[Verb]'], option, "Adjective", grammar)
        try:
            next(y)
            next(y)
            file_1.close()
        except StopIteration:
            file_1.close()


if __name__ == "__main__":
    unittest.main()