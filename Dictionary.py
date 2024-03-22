from Token import Token

class Dictionary:
    NUMERIC_CHARACTERS  = '0123456789.'

    # TOKEN TYPES
    INTEGER             = 'INT'
    FLOAT               = 'FLOAT'
    PLUS                = 'PLUS'
    MINUS               = 'MINUS'
    MULTIPLICATION      = 'MULT'
    DIVISION            = 'DIV'
    LEFT_PARENTHESES    = 'L_PRNTH'
    RIGHT_PARENTHESES   = 'R_PRNTH'

    operators = {
        '+': Token(PLUS),
        '-': Token(MINUS),
        '*': Token(MULTIPLICATION),
        '/': Token(DIVISION),
        '(': Token(LEFT_PARENTHESES),
        ')': Token(RIGHT_PARENTHESES)
    }