# To keep track of the current position in the input file (row and column number)
class Position:
    def __init__(self, row, column, index):
        self.row = row
        self.column = column
        self.index = index

    # Advance to next index and update row and column numbers
    def update(self, current_character):
        self.column += 1
        self.index += 1

        if current_character == "\n":
            self.row += 1
            self.column = 0     # Reset column number

        return self
    
    def __str__(self):
        # to get the correct row and column number, we add 1 to each, since they are zero-indexed
        return f"line {self.row + 1}, column {self.column + 1}"
    