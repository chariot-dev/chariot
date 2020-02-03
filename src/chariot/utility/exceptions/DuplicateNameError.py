from chariot.utility.exceptions import ErrorStrings


class NoIdentifierError(Exception):
    def __init__(self, deviceType: str, identifier: str = ''):
        self.identifier = identifier
        self.deviceType = deviceType

    def __str__(self):
        return ErrorStrings.ERR_Not_Unique_Name(self.identifier, self.deviceType)
