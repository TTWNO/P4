import os
import logging
import argparse

from  Lexer import Lexer
# setting basic config so we can log some debug information throughout the program
logging.basicConfig(level=logging.DEBUG)

# this is what we want to call in each file, to get a specific logger for that part of the compiler.
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    args = parser.parse_args()

    if not args.source:
        parser.print_help()
        return
    
    if not os.path.exists(args.source):
        logger.error(f"File '{args.source}' not found.")
        return
    logger.info(f"Compiling {args.source}")
    f = open(args.source, "r")
    program_contents = f.read()
    f.close()
    tokens = Lexer.analyze(program_contents)
    logger.debug(f"Tokens:\n{tokens}")


if __name__ == '__main__':
    main()      
