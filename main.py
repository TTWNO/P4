from Lexer import Lexer

print("Tokenizor ('exit' to quit):")

while True:
    try:
        text_input = input('> ')
        if text_input == 'exit':
            break
        result = Lexer.analyze(text_input)
        print(result)
    except Exception as e:
        print(e)
        break