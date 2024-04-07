import os
import logging
import argparse

from lexer import Lexer
from custom_parser import Parser
from code_generator import CodeGenerator

# Setting basic config so we can log some debug information throughout the program
logging.basicConfig(level = logging.DEBUG)

# This is what we want to call in each file, to get a specific logger for that part of the compiler.
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description = 'Compile a program')
    parser.add_argument('source', help = 'Source file')
    parser.add_argument('-o', '--output', help = 'Output file')
    args = parser.parse_args()

    if not args.source:
        parser.print_help()
        return
    if not os.path.exists(args.source):
        logger.error(f"File '{args.source}' not found.")
        return
    if args.output:
        if not args.output.endswith('.py'):
            logger.error("Output file must be a Python file.")
            return
        if os.path.exists(args.output):
            logger.error(f"Output file '{args.output}' already exists.")
            return

    logger.info(f"Compiling {args.source}")

    # Read the contents of the file
    f = open(args.source, "r")
    program_contents = f.read()     # Returns a string
    f.close()

    # Make sure we use the correct line endings (only \n instead of \r\n)
    # This is to support both Windows and Unix (MacOS) line endings
    program_contents.replace("\r\n", "\n")

    # Tokenize the program if contents are not empty
    if program_contents:
        lexer = Lexer(program_contents)
        tokens = lexer.tokenize()

        # Print error if token list comes back empty
        if not tokens:
            logger.error("Lexical analysis failed!")
            return
    else:
        logger.error("Empty file!")
        return

    # Parse tokens
    logger.debug(f"Tokens:\n{tokens}")
    parser = Parser(tokens)
    parsing_result = parser.parse()

    if not parsing_result:
        logger.error("Parsing failed!")
        return

    # Generate code
    logger.debug(f"Result: {parsing_result}")
    logger.info("Generating code...")
    code_generator = CodeGenerator(parsing_result)
    python_code = code_generator.generate()

    if not python_code:
        logger.error("Code generation failed!")
        return

    logger.info("Code generation complete.")
    logger.info(f"Python code:\n{python_code}")

    if args.output:
        logger.info(f"Writing to {args.output}")
        f = open(args.output, "w")
        f.write(python_code)
        f.close()
        logger.info("Done.")

if __name__ == '__main__':
    main()