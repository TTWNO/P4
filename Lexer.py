from IllegalCharacterException import IllegalCharacterException
from Position import Position
from Token import Token
from Dictionary import Dictionary

OPERATOR_DICTIONARY = Dictionary.operators
FLOAT               = Dictionary.FLOAT
INTEGER             = Dictionary.INTEGER
NUMERIC_CHARACTERS  = Dictionary.NUMERIC_CHARACTERS

class Lexer:
    def __init__(self, input):
        self.input = input                          # Input string
        self.position = Position(0, -1, -1)     # Current position in the input file
        self.current_character = None               # Current character in the input
        self.next_character()                       # Advance to the first character

    @staticmethod
    def analyze(text_input):
        lexer = Lexer(text_input)
        tokens = lexer.tokenize()
        return tokens

    # Advance to the next character in the input
    def next_character(self):
        self.position.update(self.current_character)
        if self.position.index < len(self.input):
            self.current_character = self.input[self.position.index]
        else:
            self.current_character = None       # Reached the end of input

    def tokenize(self):
        tokens = []

        while self.current_character is not None:
            if self.current_character in NUMERIC_CHARACTERS:
                tokens.append(self.digitize())
            elif self.current_character in OPERATOR_DICTIONARY:
                tokens.append(OPERATOR_DICTIONARY[self.current_character])
                self.next_character()
            elif self.current_character in " \n\t":             # Ignore whitespaces and tabs
                self.next_character()
            else:
                raise IllegalCharacterException("IllegalCharacterException", self.current_character, self.position)

        return tokens

    # Converting a sequence of digit characters into a numerical token (integer or float)
    def digitize(self):
        isFloat = False
        numeral_string = ""

        # Loop the input string until a non-digit character is found
        while (self.current_character is not None) and (self.current_character in NUMERIC_CHARACTERS):
            if self.current_character == ".":
                # Check if the value already has a dot (is a float)
                if isFloat:
                    break
                else:
                    numeral_string += "."
                    isFloat = True
            else:
                numeral_string += self.current_character

            self.next_character()

        if isFloat:
            return Token(FLOAT, float(numeral_string))
        else:
            return Token(INTEGER, int(numeral_string))