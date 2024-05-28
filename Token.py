class Token:
    # Token constructor
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    # Overriding the string representation method (so it looks nice in the terminal)
    def __repr__(self):
        # Return the type and value if the token has a value
        if self.value:
            return f"{self.type}:{self.value}"
        else:
            return f"{self.type}"

    # Overriding the equality method (so we can compare tokens during unit testing)
    def __eq__(self, other):
        # Compare the type and value if the other object is a token,
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        else:
            return False
