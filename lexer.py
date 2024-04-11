import logging

from position import Position
from Token import Token
from dictionary import Dictionary

OPERATOR_DICTIONARY     = Dictionary.operators
#MULTI_WORD_OPERATORS    = set(Dictionary.multi_word_operators)
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

    # Move focus back to the previous character in the input
    def previous_character(self):
        # Decrement position
        self.position.decrement(self.current_character)

        # Update current character
        if self.position.index >= 0:
            self.current_character = self.input_string[self.position.index]

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
                generated_token = self.keyword_tokenize()
                if generated_token is not None:
                    tokens.append(self.keyword_tokenize())
                else:
                    return None
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
        if alphanumerical_string in Dictionary.KEYWORDS:
            if alphanumerical_string != "is":
                return Token(Dictionary.KEYWORD, alphanumerical_string)
            else: # first part of a multi-word operator
                multi_word_keyword = "is "
                self.next_character() # skip whitespace after is
                while True:
                    word = self.peek_until_escape_character()
                    if word in Dictionary.multi_word_keyword_parts:
                        multi_word_keyword += word + " "
                        continue
                    else: 
                        multi_word_keyword = multi_word_keyword.strip() # remove trailing space in the string
                        self.go_back_n(len(word) + 1) # go back to before the token we couldn't use, so this loop doesn't swallow it
                        break
                
                # we have a multi-word keyword to work with.
                if multi_word_keyword not in Dictionary.multi_word_keywords:
                    # there was an error in the input
                    self.go_back_n(len(multi_word_keyword))
                    logger.error(f"Syntax error: Invalid multi-word operator: {multi_word_keyword} at {self.position}")
                    return None
                
            if multi_word_keyword in Dictionary.multi_word_operators:
                return Token(Dictionary.multi_word_operators[multi_word_keyword], multi_word_keyword)
           
        else: # it wasn't a keyword, so it must be an identifier
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
        
    # Peeks n-characters ahead and returns the string
    def peek_n(self, n):
        if self.position.index + n < len(self.input_string):
            return self.input_string[self.position.index:self.position.index + n]
        else:
            return None
        
    # Peek until white space or escape character is found
    def peek_until_escape_character(self):
        peeked_string = ""
        while True:
            temp_string = self.peek()
            if temp_string in ESCAPE_DICTIONARY:
                self.next_character()
                break
            peeked_string += temp_string
            self.next_character()
            
        return peeked_string
        
    # Advance n-characters in the input
    def advance_n(self, n):
        for _ in range(n):
            self.next_character()

    # Go back n-characters in the input
    def go_back_n(self, n):
        for _ in range(n):
            self.previous_character()