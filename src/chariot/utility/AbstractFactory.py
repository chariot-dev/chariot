from typing import Any, Dict, Type
from chariot.configuration.Configuration import Configuration


class AbstractFactory:
    def __init__(self):
        self.instanceMap: Dict[str, Type] = {}
        # override this for more descriptive error messages
        self.instanceName: str = 'instance'

    def getInstance(self, config: Type[Configuration]) -> Any:
        instanceType: str = config.type
        if instanceType not in self.instanceMap:
            raise AssertionError(
                'Unsupported {self.instanceName} type "{instanceType}"')
        instance: Any = self.instanceMap[instanceType](config)
        return instance


__all__ = ['AbstractFactory']
