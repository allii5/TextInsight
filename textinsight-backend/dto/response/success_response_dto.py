from dto.response.base_repsonse_dto import BaseResponseDTO

class SuccessResponseDTO(BaseResponseDTO):
    def __init__(self, message: str, status_code: int, data=None):
        super().__init__(message, success=True, status_code=status_code, data=data)