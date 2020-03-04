from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONDict, JSONObject
from typing import Dict, Type


class NetworkConfiguration(Configuration):
    requiredFields: Dict[str, Type[JSONObject]] = {
        'networkName': str,
    }

    optionalFields: Dict[str, Type[JSONObject]] = {
        'description': str,
    }

    def getId(self) -> str:
        return getattr(self, 'networkName')

    def getIdField(self) -> str:
        return 'networkName'


__all__ = ['NetworkConfiguration']
