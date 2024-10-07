class HipcallAPIException(Exception):
    def __init__(self, status_code: int, content: dict):
        self.status_code = status_code
        self.content = content

    def __str__(self):
        return f"Unexpected error. Status: {self.status_code}, Content: #{self.content}"


class BadRequestException(HipcallAPIException):
    def __str__(self):
        return f"Bad request: {self.content["errors"]["detail"]}"


class UnauthorizedException(HipcallAPIException):
    def __str__(self):
        return "Invalid API key or unauthorized access"


class NotFoundException(HipcallAPIException):
    def __str__(self):
        return "The requested resource was not found"


class UnprocessableEntityException(HipcallAPIException):
    def __str__(self):
        errors = " | ".join(
            [f"{k}: {', '.join(v)} " for k, v in self.content["errors"]]
        )
        return f"The request was unprocessable: Errors: {errors}"
