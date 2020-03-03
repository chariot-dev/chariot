class DatabaseConnectionError(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message


class DeviceNotSupported(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message


class DuplicateNameError(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message


class NameNotFoundError(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message


class NoIdentifierError(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message
