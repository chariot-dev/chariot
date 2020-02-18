from typing import Dict, List, Type

from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.database.DatabaseConfiguration import DatabaseConfiguration


class MySQLDatabaseConfiguration(DatabaseConfiguration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'username': str,
        'password': str,
        'database': str,
    }

    optionalFields: Dict[str, Type[JSONObject]] = {}

    def __init__(self, configMap: JSONDict):
        self.requiredFields.update(super().requiredFields)
        self.optionalFields.update(super().optionalFields)
        super().__init__(configMap)

    def _validateInitialConfig(self, configMap: JSONDict) -> None:
        super()._validateInitialConfig(configMap)
        if configMap['databaseType'] != 'MySQL':
            raise AssertionError(
                'Incorrect database type for use with MySQL writer')
