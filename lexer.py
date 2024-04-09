import logging

from position import Position
from Token import Token
from dictionary import Dictionary

OPERATOR_DICTIONARY     = Dictionary.operators
ESCAPE_DICTIONARY       = Dictionary.escape_characters
FLOAT                   = Dictionary.FLOAT
INTEGER                 = Dictionary.INTEGER
NUMERIC_CHARACTERS      = set(Dictionary.NUMERIC_CHARACTERS)
ALPHABETIC_CHARACTERS   = set(Dictionary.ALPHABETIC_CHARACTERS)

logger = logging.getLogger(__name__)

class Lexer:
    def __init__(self, input):
        self.input_string = input                           # Input file as a string
        self.position = Position(0, 0, 0)                   # Current row and column of file (and index of input string)
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

    # Return a list of tokens from the input string
    def tokenize(self):
        tokens = []

        # Loop through the input string and tokenize accordingly
        while self.current_character is not None:
            # Digits
            if self.current_character in NUMERIC_CHARACTERS:
                tokens.append(self.digit_tokenize())
            # Operators
            elif self.current_character in OPERATOR_DICTIONARY:
                tokens.append(OPERATOR_DICTIONARY[self.current_character])
            # Keywords and identifiers
            elif self.current_character in ALPHABETIC_CHARACTERS:
                tokens.append(self.keyword_tokenize())
            # White spaces and escape characters
            elif self.current_character in ESCAPE_DICTIONARY:
                tokens.append(self.escape_tokenize())
            else:
                logger.error(f"Illegal character: \'{self.current_character}\' at {self.position}")
                return None

            self.next_character()

        return tokens

    # Convert a possible sequence of digits into a numerical token (integer or float)
    def digit_tokenize(self):
        is_float = False
        numeral_string = ""

        # Loop the input string until a non-digit character is found
        while (self.current_character is not None) and (self.current_character in NUMERIC_CHARACTERS):
            if self.current_character == ".":
                # Break out if value (numeral_string) already is a float
                if "." in numeral_string:
                    break
                else:
                    numeral_string += "."
                    is_float = True
            else:
                numeral_string += self.current_character

            # Break out if next character is not a digit
            if self.peek() not in NUMERIC_CHARACTERS:
                break
            else:
                self.next_character()

        # Return integer or float token
        if is_float:
            return Token(FLOAT, float(numeral_string))
        else:
            return Token(INTEGER, int(numeral_string))

    # TODO: implement support for multi-word logical operators like 'is equal to', 'is not', etc.
    # Tokenize keywords and identifiers
    def keyword_tokenize(self):
        alphanumerical_string = ""

        # Loop the input string for a sequence of alphabetic characters
        while (self.current_character is not None) and (self.current_character in ALPHABETIC_CHARACTERS or self.current_character in NUMERIC_CHARACTERS):
            alphanumerical_string += self.current_character
            
            # Break out on white spaces and escape characters
            if self.peek() in ESCAPE_DICTIONARY:
                break
            else:
                self.next_character()

        # Return keyword or identifier token
        if alphanumerical_string in OPERATOR_DICTIONARY:
            return OPERATOR_DICTIONARY[alphanumerical_string]       # This doens't work as we break out on white spaces...
        elif alphanumerical_string in Dictionary.KEYWORDS:
            return Token(Dictionary.KEYWORD, alphanumerical_string)
        else:
            return Token(Dictionary.IDENTIFIER, alphanumerical_string)

    # Tokenize white spaces and escape characters (newline and tab)
    def escape_tokenize(self):
        return ESCAPE_DICTIONARY.get(self.current_character)
    
    # Return the next character in the input without advancing the focus
    def peek(self):
        if self.position.index + 1 < len(self.input_string):
            return self.input_string[self.position.index + 1]
        else:
            return None