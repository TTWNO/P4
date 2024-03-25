import sys

from IllegalCharacterException import IllegalCharacterException
from Lexer import Lexer

FILE = "text_input.txt"

try:
    with open(FILE, "r") as file:
        text_input = file.read()

    result = Lexer.analyze(text_input)
    print(result)
except IllegalCharacterException as e:
    sys.stderr.write(str(e))
except FileNotFoundError:
    print(f"File '{FILE}' not found.")
