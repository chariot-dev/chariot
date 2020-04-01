from typing import Dict, Type
from chariot.configuration import Configuration
from chariot.utility.JSONTypes import JSONObject


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
