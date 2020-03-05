from chariot.database.configuration import DatabaseConfiguration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from typing import Dict, List, Type


class MongoDatabaseConfiguration(DatabaseConfiguration):
    requiredFields: Dict[str, Type[JSONObject]] = {}

    optionalFields: Dict[str, Type[JSONObject]] = {
        'username': str,
        'password': str,
    }

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(configMap)
        if not hasattr(self, 'port'):
            # https://docs.mongodb.com/manual/reference/connection-string/
            setattr(self, 'port', 27017)

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        super()._validateInitialConfig(configMap)
        if configMap['type'] != 'MongoDB':
            raise AssertionError(
                'Incorrect database type for use with MongoDB writer')
        if 'username' in configMap and 'password' not in configMap:
            raise ValueError('"username" was supplied but "password" was not')
        if 'password' in configMap and 'username' not in configMap:
            raise ValueError('"password" was supplied but "username" was not')
