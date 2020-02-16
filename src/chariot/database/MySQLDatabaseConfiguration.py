from chariot.JSONTypes import JSONDict, JSONObject
from chariot.database.DatabaseConfiguration import DatabaseConfiguration


class MySQLDatabaseConfiguration(DatabaseConfiguration):
    def __init__(self, configMap: JSONDict):
        self.validateConfig(configMap)
        self.configMap = configMap

    def validateConfig(self, configMap: JSONDict):
        if configMap['databaseType'] != 'MySQL':
            raise AssertionError

        requiredFields: Dict[str, Type[JSONObject]] = {
            'username': str,
            'password': str,
            'database': str,
        }

        for field in requiredFields:
            fieldType = requiredFields[field]
            if field not in configMap or not isinstance(
                    configMap[field], fieldType):
                raise ValueError
