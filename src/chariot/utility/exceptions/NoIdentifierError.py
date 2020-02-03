from core.exceptions import ErrorStrings


class NoIdentifierError(Exception):
    def __init__(self, identifier=''):
        self.identifier = identifier;

    def __str__(self):
        return ErrorStrings.ERR_Specify_Identifier(self.identifier)

