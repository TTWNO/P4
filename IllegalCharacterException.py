class IllegalCharacterException(Exception):
    def __init__(self, exception_name, message, position):
        super().__init__("Illegal character", message)
        self.exception_name = exception_name
        self.message = message
        self.position = position

    def __str__(self):
        return f"{self.exception_name}: {self.message}" + f"\t(row: {self.position.row + 1}, column: {self.position.column + 1})"