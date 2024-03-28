import logging

from position import Position
from Token import Token
from dictionary import Dictionary

OPERATOR_DICTIONARY = Dictionary.operators
FLOAT               = Dictionary.FLOAT
INTEGER             = Dictionary.INTEGER
NUMERIC_CHARACTERS  = Dictionary.NUMERIC_CHARACTERS

logger = logging.getLogger(__name__)

class Lexer:
    def __init__(self, input):
        self.input_string = input                           # Input file as a string
        self.position = Position(0, 0, 0)   # Current row, column of file (and index of string)
        self.current_character = self.input_string[0]       # Current character in focus

    # Advance focus to the next character in the input
    def next_character(self):
        # Increment position
        self.position.increment(self.current_character)

        # Check if we have reached the end of the input
        if self.position.index < len(self.input_string):
            # If not, update current character
            self.current_character = self.input_string[self.position.index]
        else:
            self.current_character = None       # Reached the end of input

    # Return a list of tokens from the input
    def tokenize(self):
        tokens = []

        # Loop through the input
        while self.current_character is not None:
            # Handle a digit or possible and return appropriate token type (integer or float)
            if self.current_character in NUMERIC_CHARACTERS:
                # Handle the digit (and possible sequence of digits) and then append to the tokens list
                tokens.append(self.digitize())
            elif self.current_character in OPERATOR_DICTIONARY:
                tokens.append(OPERATOR_DICTIONARY[self.current_character])
                self.next_character()
            # Ignore whitespaces and tabs
            elif self.current_character in " \n\t":
                self.next_character()
            else:
                logger.error(f"Illegal character: \'{self.current_character}\' at {self.position}")
                return None

        return tokens

    # Convert a possible sequence of digits into a numerical token (integer or float)
    def digitize(self):
        is_float = False
        numeral_string = ""

        # Loop the input string until a non-digit character is found
        while (self.current_character is not None) and (self.current_character in NUMERIC_CHARACTERS):
            if self.current_character == ".":
                # Check if the value (numeral_string) already has a dot (is a float)
                if "." in numeral_string:
                    break
                else:
                    numeral_string += "."
                    is_float = True
            else:
                numeral_string += self.current_character

            self.next_character()

        if is_float:
            return Token(FLOAT, float(numeral_string))
        else:
            return Token(INTEGER, int(numeral_string))