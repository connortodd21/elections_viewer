class InvalidInputError(Exception):
    """Exception raised for invalid user input."""

    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message) # Call the parent's constructor

    def __str__(self):
        return f"message: {self.message}"