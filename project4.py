# project4.py
#
# ICS 33 Spring 2023
# Project 4: Still Looking for Something
import random
from pathlib import Path


def main() -> None:
    grammar_file = Path(input())
    num_of_sentences = int(input())
    start_variable = input()
    file_1 = open(grammar_file, "r")
    grammar = Grammar()
    grammar.grammar_object = grammar
    grammar.store_rules(file_1)

    # quit_file = # function where making the object starts
    # if quit_file is True:
    # file_1.close()


# So when the first time goes through, I'll call it with the
# grammar class for current_class. When the grammar class method
# is called, it only needs the start variable passed to it.


def call_duck_typed_method(current_sent_state, current_class, start_variable, grammar):
    yield from current_class.generate_sentence_fragment(current_sent_state, current_class, start_variable, grammar)

class TerminalSymbol:
    def __init__(self):
        pass

class VariableSymbol:
    def __init__(self):
        pass

class Option:
    def __init__(self):
        pass

class Rule:
    def __init__(self):
        pass

    def generate_random_number(self, options_of_start_variable):
        list_of_weights = []
        for option in options_of_start_variable[1:]:
            for i in range(int(option[0])):
                list_of_weights.append(option[0])
        random_num_of_list_of_weights = random.choice(list_of_weights)
        x = True
        while x is True:
            random_num_in_ops_of_start_var = random.randint(0, len(options_of_start_variable)-1)
            if options_of_start_variable[random_num_in_ops_of_start_var][0] == random_num_of_list_of_weights:
                final_option_chosen = options_of_start_variable[random_num_in_ops_of_start_var]
                x = False
        return final_option_chosen


    #go through the current sentence fragment, which at this point
    #will a list with lists inside of it, each sublist containing,
    #an option. so go through that list and add up all the first
    ##later.......

    def generate_sentence_fragment(self, options_of_start_variable, current_class):
        option_chosen = self.generate_random_number(options_of_start_variable)





class Grammar:
    def __init__(self, original_grammar=None):
        self.original_grammar = original_grammar
        self.file = []
        self.grammar_object = None

    def store_rules(self, file_1):
        try:
            file_iterable = iter(file_1)
            while True:
                next_line = next(file_iterable)
                if next_line == "{" + "\n":
                    second_list = []
                    while next_line.strip(" ") != "}\n":
                        next_line = next(file_iterable)
                        second_list.append(next_line.strip("\n").split(" "))
                    self.file.append(second_list)
                else:
                    pass
        except StopIteration:
            self.file.append(second_list)

    def generate_sentence_fragment(self, search_for_variable, next_class, starter_variable, gram_object):
        options_of_search_variable = []
        for next_line in self.file:
            if next_line[0][0] == starter_variable:
                options_of_search_variable = next_line
        rule = Rule()


if __name__ == '__main__':
    main()