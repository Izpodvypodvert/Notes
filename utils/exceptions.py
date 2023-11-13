class BusinessRuleViolation(Exception):
    """Exception raised when a business rule is violated."""

    def __init__(self, message: str, payload: dict = {}):
        self.message = message
        self.payload = payload
        super().__init__(self.message)

    def __str__(self):
        return (
            f"{self.message} | Payload: {self.payload}"
            if self.payload
            else self.message
        )
