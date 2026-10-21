class HipcallAPIException(Exception):
    def __init__(self, status_code: int, content: dict | None):
        self.status_code = status_code
        self.content = content

    @property
    def detail(self):
        return self.content

    @property
    def errors(self):
        """The `errors` field of the response body, if there is one."""
        if isinstance(self.content, dict):
            return self.content.get("errors")
        return None

    def __str__(self):
        return f"Unexpected error. Status: {self.status_code}, Content: {self.content}"


class BadRequestException(HipcallAPIException):
    def __str__(self):
        errors = self.errors
        if isinstance(errors, dict) and "detail" in errors:
            detail = errors["detail"]
        elif errors:
            detail = errors
        else:
            detail = self.content
        return f"Bad request: {detail}"


class UnauthorizedException(HipcallAPIException):
    def __str__(self):
        return "Invalid API key or unauthorized access"


class NotFoundException(HipcallAPIException):
    def __str__(self):
        return "The requested resource was not found"


class UnprocessableEntityException(HipcallAPIException):
    def __str__(self):
        errors = self.errors
        if isinstance(errors, dict):
            errors = " | ".join(
                f"{k}: {', '.join(v) if isinstance(v, list) else v}"
                for k, v in errors.items()
            )
        elif errors is None:
            errors = self.content
        return f"The request was unprocessable: Errors: {errors}"
