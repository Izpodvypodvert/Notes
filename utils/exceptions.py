class TooManyNotesError(Exception):
    """Exception raised when the maximum number of notes is reached."""

    def __init__(self, message: str = "You have reached the maximum number of notes allowed."):
        self.message = message
        super().__init__(self.message)
