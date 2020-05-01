from typing import Dict, Type
from chariot.configuration import Configuration
from chariot.utility.JSONTypes import JSONObject


class UserConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'username': str,
        'password': str,
        'eMail': str
    }

    optionalFields: Dict[str, Type[JSONObject]] = {
        'fullName': str,
    }

    def getId(self) -> str:
        return getattr(self, 'username')

    def getIdField(self) -> str:
        return 'username'


__all__ = ['UserConfiguration']
