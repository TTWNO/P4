"""This module contains the classes for the nodes of the abstract syntax tree (AST) of the parser."""

class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left}, {self.operator}, {self.right})"

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"
