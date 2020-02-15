from chariot.utility.exceptions.ErrorStrings import ErrorStrings


class DuplicateNameError(Exception):
    status_code = 400

    def __init__(self, identifier: str = '', errCode: int = None):
        self.identifier = identifier
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return ErrorStrings.ERR_Not_Unique_Name(self.identifier)

    def to_dict(self):
        rv = dict()
        rv["message"] = str(self.__str__)
        return rv