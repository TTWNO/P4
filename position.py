# To keep track of the current position in the input file (row and column number, and index of the input string)
class Position:
    def __init__(self, row, column, index):
        self.row = row
        self.column = column
        self.index = index

    def decrement(self, current_character):
        self.column -= 1
        self.index -= 1

    # Advance to next column and index, and possibly next row
    def increment(self, current_character):
        self.column += 1
        self.index += 1

        # Increment row and reset column if end of line is reached (newline character encountered)
        if current_character == "\n":
            self.row += 1
            self.column = 0     # Reset column number

        return self
    
    def __str__(self):
        # To get the correct row and column number, we add 1 to each, since they are zero-indexed
        return f"line {self.row + 1}, column {self.column + 1}"
    