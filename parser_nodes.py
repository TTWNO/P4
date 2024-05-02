"""This module contains the classes for the nodes of the abstract syntax tree (AST) of the parser."""

class Node:
    """Base class for all nodes in the AST."""
    pass

class IndentationNode(Node):
    """Class for nodes that represent indentation."""
    def __init__(self, value):
        self.value = value

class ExpressionNode(Node):
    """Class for nodes that represent expressions, such as mathematical operations."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ExpressionNode({self.left}, {self.operator}, {self.right})"

    def __str__(self):
        return self.__repr__()

class NumberNode(Node):
    """Class for nodes that represent numbers (int)."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"
    
    def __str__(self):
        return self.__repr__()

class IfNode(Node):
    """Class for nodes that represent if statements."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"IfNode({self.condition}, {self.body})"
    
    def __str__(self):
        return self.__repr__()

class AssignmentNode(Node):
    """Class for nodes that represent variable assignments."""
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"AssignmentNode({self.identifier}, {self.value})"
    
    def __str__(self):
        return self.__repr__()
    