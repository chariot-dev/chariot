from chariot.utility.exceptions.ErrorStrings import ErrorStrings


class NoIdentifierError(Exception):
    status_code = 400

    def __init__(self, msg: str, errCode: int = None):
        self.message = msg
        if errCode is not None:
            self.status_code = errCode

    def __str__(self):
        return self.message

    def to_dict(self):
        rv = dict()
        rv["message"] = self.__str__()
        return rv

