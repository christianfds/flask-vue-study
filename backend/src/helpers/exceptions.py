class ServiceException(Exception):
    status = 400


class ValidationException(ServiceException):
    pass