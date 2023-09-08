# project4.py
#
# ICS 33 Spring 2023
# Project 4: Still Looking for Something
import random
from pathlib import Path

def main(testing=False) -> None:
    """This method called the function that asks for input.
    """
    return ask_for_inputs(testing)

def random_name_gen(start_var, testing=False):
    return ask_for_inputs(testing, start_var)

def ask_for_inputs(testing, start_var):
    """This function asks for the three inputs required by the user.
    """
    grammar_file = "test_file.txt"
    #num_of_sentences = int(input("Enter the number of sentences you want to output: "))
    #start_variable = input("Enter the start variable for the output sentences(Some examples are LetStatement, PrintStatement, GosubStatement): ")
    num_of_sentences = 1
    start_variable = start_var
    file_1 = open(grammar_file, "r")
    grammar = Grammar()
    grammar.grammar_object = grammar
    grammar.store_rules(file_1)
    return calling_loop(num_of_sentences, grammar, start_variable, testing, file_1)

def calling_loop(num_of_sentences, grammar, start_variable, testing, file_1):
    """This function contains the for loop that calls on the generator object
    yielded frm the duck typed method. It checks whether the thing yielded back
    is a terminal and if it is, it's added to the list After the loop is finished
    the output is printed."""
    for num in range(num_of_sentences):
        x = call_duck_typed_method(["1", "[]"], grammar, start_variable, grammar)
        string_list = []
        string_to_print = ""
        for i in x:
            if i.startswith("[") is False and i.endswith("]") is False or i.isalnum() is False:
                string_list.append(i)
        for symbol in string_list:
            string_to_print += f" {symbol}"
        #print(string_to_print[1:])
        return (string_to_print[1:])
    if testing is True:
        file_1.close()

def call_duck_typed_method(current_sent_state, current_class, start_variable, grammar):
    """This function calls the method that is sent to it based off of the class
    that is gets. This is where I use duck typing because this function has one
    line that calls 4-5 different methods in my code."""
    yield from current_class.generate_sentence_fragment(current_sent_state, current_class, start_variable, grammar)

class TerminalSymbol:
    """Contains the terminal functionality."""

    def generate_sentence_fragment(self, current_sent_frag, current_class, starter_variable, gram_object, index):
        """This function returns a terminal so that it can be added to the list and printed
        after all terminals have been collected."""

        return current_sent_frag[index]

class VariableSymbol:
    """Contains the variable functionality."""

    def generate_sentence_fragment(self, current_sent_frag, current_class, starter_variable, gram_object, index):
        """This method yields back to the duck type method
        so that it can be sent to the grammar class. This
        happens so that the program can recurse a level deeper
        and find what to replace the variable with."""
        searching_for = current_sent_frag[index][1:-1]
        yield from call_duck_typed_method(starter_variable, gram_object, searching_for, gram_object)

class Option:
    """Contains the Option functionality."""

    def generate_sentence_fragment(self, current_sent_frag, current_class, starter_variable, gram_object):
        """This method goes through the current sentence fragment, symbol by symbol,
        to check whether the symbol is a variable or a terminal. The program is sent
        to the corresponding class from there."""
        for index in range(len(current_sent_frag)):
            if current_sent_frag[index].startswith("[") and current_sent_frag[index].endswith("]") and current_sent_frag[index][1:-1].isalnum():
                variable = VariableSymbol()
                yield from variable.generate_sentence_fragment(current_sent_frag, current_class, starter_variable, gram_object, index)
            else:
                terminal = TerminalSymbol()
                yield terminal.generate_sentence_fragment(current_sent_frag, current_class, starter_variable, gram_object, index)

class Rule:
    """Contains the Rule functionality."""
    def generate_random_number(self, options_of_start_variable):
        """This method chooses a random option from the possible options
        in a rule for a variable. This option is then returned back so that
        it can be yielded to the option class."""
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


    def generate_sentence_fragment(self, options_of_start_variable, current_class, starter_variable, gram_object):
        """This method calls the generate number method. After getting the option
        returned, it yields that option back to the duck typed method."""
        option_chosen = self.generate_random_number(options_of_start_variable)
        option = Option()
        yield from call_duck_typed_method(option_chosen[1:], option, starter_variable, gram_object)


class Grammar:
    """Contains the Grammar functionality."""
    def __init__(self, original_grammar=None):
        """Stores the original grammar, file, and the
        grammar object so that it can be used."""
        self.original_grammar = original_grammar
        self.file = []
        self.grammar_object = None


    def store_rules(self, file_1):
        """This method goes through the text file
        and parses it in a way that is easily organized
        by the curly brackets, separating each set of rules."""
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

    def generate_sentence_fragment(self, search_for_variable, next_class, matching_variable, gram_object):
        """This method goes through the saved file until it reaches the line that has the variable
        that it's trying to match with."""
        options_of_search_variable = []
        for next_line in self.file:
            if next_line[0][0] == matching_variable:
                options_of_search_variable = next_line
        rule = Rule()
        yield from call_duck_typed_method(options_of_search_variable[0:-1], rule, matching_variable, gram_object)
