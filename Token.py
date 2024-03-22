class Token:
    # Token constructor
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    # Overriding the string representation method (so it looks nice in the terminal)
    def __repr__(self):
        if self.value:      # If the token has a value, return the type and value
            return f"{self.type}:{self.value}"
        else:
            return f"{self.type}"