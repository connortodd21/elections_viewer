class DataNotGeneratedException(Exception):
    """Exception raised when the data requested has not been generated yet for a state or county."""

    EXCEPTION_MESSAGE = "Data for {} has not been generated yet. Please try again later."

    def __init__(self, location: str) -> None:
        self.message = self.EXCEPTION_MESSAGE.format(location)
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"message: {self.message}"