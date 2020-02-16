from chariot.JSONTypes import JSONDict, JSONObject
from chariot.database.DatabaseConfiguration import DatabaseConfiguration


class MongoDatabaseConfiguration(DatabaseConfiguration):
    def __init__(self, configMap: JSONDict):
        self.validateConfig(configMap)
        self.configMap = configMap

    def validateConfig(self, configMap: JSONDict):
        if configMap['databaseType'] != 'MongoDB':
            raise AssertionError

        optionalFields: Dict[str, Type[JSONObject]] = {
            'username': str,
            'password': str,
            'database': str,
        }

        for field in optionalFields:
            fieldType = optionalFields[field]
            if field in configMap and not isinstance(
                    configMap[field], fieldType):
                raise ValueError

        # no username without password, or vice versa
        if 'username' in configMap and 'password' not in configMap:
            raise ValueError
        if 'password' in configMap and 'username' not in configMap:
            raise ValueError
