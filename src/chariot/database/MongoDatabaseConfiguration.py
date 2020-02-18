from typing import Dict, List, Type

from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.database.DatabaseConfiguration import DatabaseConfiguration


class MongoDatabaseConfiguration(DatabaseConfiguration):
    requiredFields: Dict[str, Type[JSONObject]] = {}

    optionalFields: Dict[str, Type[JSONObject]] = {
        'username': str,
        'password': str,
        'database': str
    }

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(configMap)

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        super()._validateInitialConfig(configMap)
        if configMap['databaseType'] != 'MongoDB':
            raise AssertionError(
                'Incorrect database type for use with MongoDB writer')
        # no username without password, or vice versa
        if 'username' in configMap and 'password' not in configMap:
            raise ValueError(
                "If username is supplied, password must also be supplied")
        if 'password' in configMap and 'username' not in configMap:
            raise ValueError(
                "If username is supplied, password must also be supplied")
