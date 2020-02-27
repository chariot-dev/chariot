from abc import ABC
from typing import Any, Dict, Type, Union
from chariot.configuration.Configuration import Configuration
from chariot.utility.JSONTypes import JSONObject


class AbstractFactory(ABC):
    def __init__(self):
        self.instanceMap: Dict[str, Type] = {}
        # override this for more descriptive error messages
        self.typeField: str = 'type'
        self.instanceName: str = 'instance'

    def getInstance(self, config: Union[Dict[str, JSONObject], Configuration]) -> Any:
        instanceType: str = str()
        if isinstance(config, Dict):
            instanceType = config.get(self.typeField)
        else:
            instanceType: str = getattr(config, self.typeField)
        if instanceType not in self.instanceMap:
            raise AssertionError(f'Unsupported {self.instanceName} type "{instanceType}"')
        instance: Any = self.instanceMap[instanceType](config)
        return instance


__all__ = ['AbstractFactory']
