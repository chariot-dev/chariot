# Chariot Exceptions Library


# TODO: pass in arguments to the error signifying the violating network/device
class DeviceNotConnectedError(AssertionError):
    def __init__(self):
        super().__init__('Device is not connected to the network.')


class InCollectionEpisodeError(AssertionError):
    def __init__(self):
        super().__init__('Network is in a Collection Episode.')


class NotInCollectionEpisodeError(AssertionError):
    def __init__(self):
        super().__init__('Network is not in a Collection Episode.')


class FailedToBeginCollectionError(Exception):
    def __init__(self):
        super().__init__('Data Collection could not be started')


class DatabaseConnectionError(Exception):
    statusCode = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.statusCode = errCode

    def __str__(self):
        return self.message


class ItemNotSupported(Exception):
    statusCode = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.statusCode = errCode

    def __str__(self):
        return self.message


class DuplicateNameError(Exception):
    statusCode = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.statusCode = errCode

    def __str__(self):
        return self.message


class NameNotFoundError(Exception):
    statusCode = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.statusCode = errCode

    def __str__(self):
        return self.message


class NoIdentifierError(Exception):
    statusCode = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.statusCode = errCode

    def __str__(self):
        return self.message


# __all__ = ['DatabaseConnectionError', 'DuplicateNameError', 'ItemNotSupported', 'NameNotFoundError', 'NoIdentifierError',
#     'DeviceNotConnectedError', 'InCollectionEpisodeError', 'NotInCollectionEpisodeError', 'FailedToBeginCollectionError']
