# project4.py
#
# ICS 33 Spring 2023
# Project 4: Still Looking for Something
import random
from pathlib import Path


def main() -> None:
    grammar_file = Path(input())
    #num_of_sentences = int(input())
    start_variable = input()
    file_1 = open(grammar_file, "r")
    grammar = Grammar()
    grammar.generate_sentence_fragment(start_variable, file_1)
    # del(options_of_start_variable[-1])
    # print(options_of_start_variable)
    # print(options_of_start_variable[0])
    # print(options_of_start_variable[1])
    # quit()

    # quit_file = # function where making the object starts
    # if quit_file is True:
    # file_1.close()


# So when the first time goes through, I'll call it with the
# grammar class for current_class. When the grammar class method
# is called, it only needs the start variable passed to it.


class Recursion:
    def __init(self, current_class=None, previous_class=None):
        self.current_class = current_class
        self.previous_class = previous_class
    def recursive_function(self, current_sentence, next_class):
        print(current_sentence)
        quit()
        #if no terminals:
            #print(current_sentence)
        #else:
            #current_class.generate_sentence_fragment(current_sentence, next_class)


'''
class TerminalSymbol:
    def __init__(self):
        pass
    # def generate_sentence_fragment():


class VariableSymbol:
    def __init__(self):
        pass
    def generate_sentence_fragment():
        pass

class Option:
    def __init__(self):
        pass
    def generate_sentence_fragment():
        pass
'''
class Rule:
    def __init__(self):
        pass

    def generate_random_number(self):
        pass
    #go through the current sentence fragment, which at this point
    #will a list with lists inside of it, each sublist containing,
    #an option. so go through that list and add up all the first
    ##later.......

    def generate_sentence_fragment(self, options_of_start_variable):
        pass
        #generate_random_number(options_of_start_variable)



class Grammar:
    def __init__(self, original_grammar=None):
        self.original_grammar = original_grammar

    def generate_sentence_fragment(self, search_for_variable, file_1):
        options_of_search_variable = []
        try:
            file_iterable = iter(file_1)
            while True:
                next_line = next(file_iterable)
                if next_line == search_for_variable + "\n":
                    while next_line.strip(" ") != "}\n":
                        next_line = next(file_iterable)
                        options_of_search_variable.append(next_line.strip("\n").split(" "))
        except StopIteration:
            pass
        rule = Rule()
        recurse = Recursion()
        recurse.recursive_function(options_of_search_variable, rule)


if __name__ == '__main__':
    main()