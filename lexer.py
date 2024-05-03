import sys
import logging

from position import Position
from Token import Token
from dictionary import Dictionary

# 'is greater than or equal to' is the longest multi-word operator
MAX_NUMBER_OF_OPERATOR_WORDS = 6        

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
            # Reached the end of input
            self.current_character = None       

    # Return a list of tokens from the input string
    def tokenize(self):
        tokens = []

        # Loop through the input string and tokenize accordingly
        while self.current_character is not None:
            # Digits
            if self.current_character in Dictionary.NUMERIC_CHARACTERS:
                tokens.append(self.digit_tokenize())
            # Arithmetic operators (single symbols)
            elif self.current_character in Dictionary.operators:
                tokens.append(Dictionary.operators[self.current_character])
            # Keywords, identifiers and multi-word arithmetic operators
            elif self.current_character in Dictionary.ALPHABETIC_CHARACTERS:
                tokens.append(self.keyword_tokenize())
            # White spaces and escape characters
            elif self.current_character in Dictionary.escape_characters:
                tokens.append(self.escape_tokenize())
            else:
                logger.error(f"Illegal character: \'{self.current_character}\' at {self.position}")
                sys.exit(1)

            self.next_character()

        return tokens

    # Convert a possible sequence of digits into a numerical token (integer or float)
    def digit_tokenize(self):
        is_float = False
        numeral_string = ""

        # Loop the input string until a non-digit character is found
        while (self.current_character is not None) and (self.current_character in Dictionary.NUMERIC_CHARACTERS):
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
            if self.peek() not in Dictionary.NUMERIC_CHARACTERS:
                break
            else:
                self.next_character()

        # Return integer or float token
        if is_float:
            return Token(Dictionary.FLOAT, float(numeral_string))
        else:
            return Token(Dictionary.INTEGER, int(numeral_string))

    # Tokenize keywords, identifiers and multi-word operators
    def keyword_tokenize(self):
        alphanumerical_string = ""

        # Loop the input string for a sequence of alphabetic characters
        while (self.current_character is not None) and (self.current_character in Dictionary.ALPHABETIC_CHARACTERS or self.current_character in Dictionary.NUMERIC_CHARACTERS):
            alphanumerical_string += self.current_character
            
            # Break out on white spaces and escape characters
            if self.peek() in Dictionary.escape_characters:
                break
            else:
                self.next_character()
        
        # Return appropriate token
        if alphanumerical_string == "is":
            return self.handle_multi_word_operator(alphanumerical_string)
        elif alphanumerical_string == "cell":
            return self.handle_excel_cell()
        elif alphanumerical_string in Dictionary.KEYWORDS:
            return Token(Dictionary.KEYWORD, alphanumerical_string)
        # It wasn't a keyword, so it must be an identifier   
        else: 
            return Token(Dictionary.IDENTIFIER, alphanumerical_string)

    # Return the next character in the input without advancing the focus
    def peek(self):
        if self.position.index + 1 < len(self.input_string):
            return self.input_string[self.position.index + 1]
        else:
            return None
        
    # Handle Excel cell references (e.g. 'A1', 'B2', 'C3')
    def handle_excel_cell(self):
        cell_reference = self.peek_word_ahead()
        self.advance_n(len(cell_reference))
        cell_reference = cell_reference.strip()
        # an excel cell reference is any amount of alphabetic characters followed by any amount of numeric characters
        # validating this will be handled in the parser
        # advance the focus to the end of the cell reference
        return Token(Dictionary.CELL, cell_reference)

        

    # TODO: Could potentially be made more bullet-proof in regards to syntax errors
    # Check for multi-word operators (e.g. 'is equal to', 'is greater than')
    def handle_multi_word_operator(self, alphanumerical_string):       
        # Peek ahead at most the number of words the longest multi-word operator consists of 
        # (minus the already consumed first word ('is'))
        for _ in range(MAX_NUMBER_OF_OPERATOR_WORDS - 1):
            if self.peek() is not None:
                #print(f"Peeking word ahead of: '{alphanumerical_string}'")
                peeked_word = self.peek_word_ahead()
                number_of_symbols_peeked = len(peeked_word)
                #print(f"Number of symbols peeked: {number_of_symbols_peeked}")

                # Ignore leading whitespace and check if the peeked word is a multi-word operator part
                if peeked_word[1:] in Dictionary.multi_word_operator_parts:
                    self.advance_n(number_of_symbols_peeked)
                    alphanumerical_string += peeked_word
                else:
                    break
        
        # Return either multi-word operator or assignment token (single-word operator)
        if alphanumerical_string in Dictionary.multi_word_operators:
            print(f"Returning token as multi-word operator: '{alphanumerical_string}'")
            return Token(Dictionary.multi_word_operators[alphanumerical_string])
        elif alphanumerical_string == "is":
            return Token(Dictionary.ASSIGNMENT)
        else:
            logger.error(f"Syntax error: Invalid multi-word operator: '{alphanumerical_string}' at {self.position}")
            sys.exit(1)

    # Peek a word ahead (until a white space or escape character is encountered)   
    def peek_word_ahead(self):
        peeked_word = ""
        current_index = self.position.index + 1
        
        # Skip leading white space
        if self.input_string[current_index] == ' ':
            peeked_word += ' '
            current_index += 1

        # Loop until next white space or escape character is found
        while (current_index < len(self.input_string)) and (self.input_string[current_index] not in Dictionary.escape_characters):
            peeked_word += self.input_string[current_index]
            current_index += 1

        #print(f"Peeked word: '{peeked_word}'")

        return peeked_word

    # Advance n-characters in the input
    def advance_n(self, n):
        for _ in range(n):
            self.next_character()

    # Tokenize white spaces and escape characters (newline and tab)
    def escape_tokenize(self):
        return Dictionary.escape_characters.get(self.current_character)
        




        
# Jessica's solution 
""" if alphanumerical_string in Dictionary.KEYWORDS:
            if alphanumerical_string != "is":
                print(f"Returning keyword: {alphanumerical_string}")
                return Token(Dictionary.KEYWORD, alphanumerical_string)
            else: 
                # First part of a multi-word operator
                multi_word_keyword = "is "

                # Skip whitespace after is
                self.next_character()

                while True:
                    word = self.peek_until_escape_character()
                    
                    if word in Dictionary.multi_word_operator_parts:
                        multi_word_keyword += word + " "
                        continue
                    else: 
                        # Remove trailing space in the string
                        multi_word_keyword = multi_word_keyword.strip()

                        # Go back to before the token we couldn't use, so this loop doesn't swallow it 
                        self.go_back_n(len(word) + 1) 
                        break
                
                # We have a multi-word keyword to work with.
                if multi_word_keyword not in Dictionary.multi_word_operators:
                    
                    # There was an error in the input
                    self.go_back_n(len(multi_word_keyword))
                    logger.error(f"Syntax error: Invalid multi-word operator: {multi_word_keyword} at {self.position}")
                    return None
                
                # It worked before, when we compared each multi word keyboard individually
                for x in range(len(Dictionary.multi_word_operators)):
                    print(f"Comparing {multi_word_keyword} to {Dictionary.multi_word_operators[x]}")
                    if multi_word_keyword == Dictionary.multi_word_operators[x]:
                        return Token(Dictionary.multi_word_operators[x], multi_word_keyword)
                    
                # We did not find a match in the multi-word operators
                logger.error(f"Syntax error: Invalid multi-word operator: {multi_word_keyword} at {self.position}")
                return None """

""" 
    # Move focus back to the previous character in the input
    def previous_character(self):
        # Decrement position
        self.position.decrement()

        # Update current character
        if self.position.index >= 0:
            self.current_character = self.input_string[self.position.index]

    # Peek until white space or escape character is found
    def peek_until_escape_character(self):
        peeked_string = ""
        
        while True:
            temp_string = self.peek()
            
            if temp_string in Dictionary.escape_characters or temp_string == " ":
                self.next_character()
                break
            
            print(f"Peeking: {temp_string}")
            if temp_string is None:
                break
            else:
                peeked_string += temp_string
                self.next_character()
                
        return peeked_string 
        
    # Go back n-characters in the input
    def go_back_n(self, n):
        for _ in range(n):
            self.previous_character()
"""