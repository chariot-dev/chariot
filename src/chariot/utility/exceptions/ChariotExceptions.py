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
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message


class ItemNotSupported(Exception):
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


__all__ = ['DatabaseConnectionError', 'DeviceNotSupported', 'DuplicateNameError', 'NameNotFoundError', 'NoIdentifierError', 
    'DeviceNotConnectedError', 'InCollectionEpisodeError', 'NotInCollectionEpisodeError', 'FailedToBeginCollectionError']
