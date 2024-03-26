import os
import logging
import argparse

from  Lexer import Lexer
from custom_parser import Parser
from code_generator import CodeGenerator

# setting basic config so we can log some debug information throughout the program
logging.basicConfig(level=logging.DEBUG)

# this is what we want to call in each file, to get a specific logger for that part of the compiler.
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    parser.add_argument('-o', '--output', help='Output file')
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
    f = open(args.source, "r")
    program_contents = f.read()
    f.close()
    tokens = Lexer.analyze(program_contents)
    if not tokens:
        logger.error("Compilation failed.")
        return
    logger.debug(f"Tokens:\n{tokens}")
    parser = Parser(tokens)
    parsing_result = parser.parse()
    if not parsing_result:
        logger.error("Compilation failed.")
        return
    logger.debug(f"Result: {parsing_result}")
    logger.info("Generating code...")
    code_generator = CodeGenerator(parsing_result)
    python_code = code_generator.generate()
    if not python_code:
        logger.error("Code generation failed.")
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
