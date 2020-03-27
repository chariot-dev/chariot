from chariot.configuration import Configuration
from chariot.network import Network
from chariot.database.writer import DatabaseWriter
from chariot.utility.JSONTypes import JSONDict, JSONObject
from typing import Dict, Type


class DataCollectionConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'configId': str,
        'network': Network,
        'database': DatabaseWriter,
    }

    optionalFields: Dict[str, Type[JSONObject]] = {
        'runTime': int,
    }

    def getId(self) -> str:
        return getattr(self, 'configId')

    def getIdField(self) -> str:
        return 'configId'
