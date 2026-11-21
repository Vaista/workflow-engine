from app.exceptions.exceptions.base import AppException


class OrganizationAlreadyExistsException(AppException):
    pass

class OrganizationUnitAlreadyExistsException(AppException):
    pass

class OrganizationNotFoundException(AppException):
    pass
