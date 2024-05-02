import logging

from dictionary import Dictionary

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast

    def generate(self, node=None, is_root=True):
        if node is None:
            node = self.ast
        method_name = 'generate_' + type(node).__name__
        generate_method = getattr(self, method_name, self.generic_generate)
        code = generate_method(node)
        
        if is_root:  # Check if this is the root call
            header = self.generate_header()
            footer = self.generate_footer()
            code = f"{header}\n{code}\n{footer}"
            
        return code

    def generic_generate(self, node):
        logger.error(f'No code generation method defined for {type(node).__name__}')
        return None

    def generate_header(self):
        return """
import sys
from openpyxl import load_workbook

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[1]} <excel_file>")
    sys.exit(1)

workbook = load_workbook(filename=sys.argv[1])
sheet = workbook.active
"""

    def generate_footer(self):
        return """
workbook.save(filename=sys.argv[1])
"""

    # Node-specific generation methods follow...
    def generate_NumberNode(self, node):
        return str(node.value)

    def generate_BinaryOperationNode(self, node):
        left_code = self.generate(node.left, is_root=False)
        right_code = self.generate(node.right, is_root=False)
        if node.operator == Dictionary.PLUS:
            operator = '+'
        elif node.operator == Dictionary.MINUS:
            operator = '-'
        elif node.operator == Dictionary.MULTIPLICATION:
            operator = '*'
        elif node.operator == Dictionary.DIVISION:
            operator = '/'
        else:
            logger.error(f'Unsupported operator {node.operator}')
            return None
        return f'({left_code} {operator} {right_code})'
