class CodeGenerator:
    def generate(self, node):
        method_name = 'generate_' + type(node).__name__
        generate_method = getattr(self, method_name, self.generic_generate)
        return generate_method(node)

    def generic_generate(self, node):
        raise Exception(f'No generate_ method defined for {type(node).__name__}')

    def generate_NumberNode(self, node):
        return str(node.value)

    def generate_BinaryOperationNode(self, node):
        left_code = self.generate(node.left)
        right_code = self.generate(node.right)
        if node.operator == 'PLUS':
            operator = '+'
        elif node.operator == 'MINUS':
            operator = '-'
        elif node.operator == 'MULT':
            operator = '*'
        elif node.operator == 'DIV':
            operator = '/'
        else:
            raise Exception(f'Unsupported operator {node.operator}')
        return f'({left_code} {operator} {right_code})'
