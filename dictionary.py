from Token import Token

class Dictionary:
    NUMERIC_CHARACTERS  = '0123456789.'
    ALPHABETIC_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    KEYWORDS = ['if', 'else if', 'else', 'return']

    # TOKEN TYPES
    INTEGER             = 'INT'
    FLOAT               = 'FLOAT'
    PLUS                = 'PLUS'
    MINUS               = 'MINUS'
    MULTIPLICATION      = 'MULT'
    DIVISION            = 'DIV'
    LEFT_PARENTHESES    = 'L_PRNTH'
    RIGHT_PARENTHESES   = 'R_PRNTH'
    NEWLINE             = 'NL'
    INDENTATION         = 'TAB'
    WHITE_SPACE         = 'WS'
    KEYWORD             = 'KW'
    IDENTIFIER          = 'ID'
    ASSIGNMENT          = 'ASSIGN'
    EQUAL_TO            = '=='

    operators = {
        '+': Token(PLUS),
        '-': Token(MINUS),
        '*': Token(MULTIPLICATION),
        '/': Token(DIVISION),
        '(': Token(LEFT_PARENTHESES),
        ')': Token(RIGHT_PARENTHESES),
        '=': Token(ASSIGNMENT),
        'is': Token(ASSIGNMENT),
        'is equal to': Token(EQUAL_TO)
    }

    escape_characters = {
        '\n': Token(NEWLINE),
        '\t': Token(INDENTATION),
        ' ' : Token(WHITE_SPACE)
    }