from app.exceptions.exceptions.base import AppException


class WorkflowAlreadyExists(AppException):
    pass


class WorkflowNotFound(AppException):
    pass

