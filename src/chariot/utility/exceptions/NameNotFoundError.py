from core.exceptions import ErrorStrings


class NameNotFoundError(Exception):
    def __init__(self, identifier: str = '', collection: str = '', type: str = ''):
        self.identifier = identifier
        self.collection = collection
        self.type = type

    def __str__(self):
        return ErrorStrings.ERR_Not_Found_In_Collection(self.identifier, self.deviceType)