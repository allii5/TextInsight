class BaseResponseDTO:
    def __init__(self, message: str, success: bool, status_code: int, data=None):
        self.message = message
        self.success = success
        self.status_code = status_code
        self.data = data

    def to_json(self):
        """Convert the DTO to a JSON-compatible dictionary."""
        response = {
            "message": self.message,
            "success": self.success,
            "status_code": self.status_code,
        }
        if self.data is not None:
            response["data"] = self.data
        return response