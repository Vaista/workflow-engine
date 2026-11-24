from app.exceptions.exceptions.base import AppException


class UserAlreadyExistsException(AppException):
    pass

class UserNotFoundException(AppException):
    pass