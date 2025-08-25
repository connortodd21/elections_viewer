class InvalidInputError(Exception):
    """Exception raised for invalid user input."""

    def __init__(self, message="Invalid input provided") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[message: {self.message}]"