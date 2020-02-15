from chariot.utility.exceptions.ErrorStrings import ErrorStrings


class NameNotFoundError(Exception):
    status_code = 400

    def __init__(self, type: str = '', identifier: str = '', collection: str = '', errCode: int = None):
        self.identifier = identifier
        self.collection = collection
        self.type = type
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return ErrorStrings.ERR_Not_Found_In_Collection.format(self.type, self.identifier, self.collection)

    def to_dict(self):
        rv = dict()
        rv["message"] = str(self.__str__)
        return rv
