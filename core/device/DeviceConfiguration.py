from typing import Dict, List
from json import dumps

class DeviceConfiguration:
    def __init__(self, configMap: Dict[str, ConfigValue]):
        self._requiredFields: List[str] = ['nickname']
        self._optionalFields: List[str] = []
        self.nickname: str = str()
      
        for field in self._requiredFields:
            try:
                setattr(self, field, configMap[field])
            except:
                # handle error for missing required configuration
                pass

        for field in self._optionalFields:
            value = configMap[field] if field in configMap else None
            setattr(self, field, value)

    def __str__(self) -> str:
        output: Dict[str, str] = dict()
        # can probably make this more pythonian by using dict comprehension
        # but this is more convenient for debugging
        for field in self._requiredFields:
            output[field] = getattr(self, field, None)
        for field in self._optionalFields:
            output[field] = getattr(self, field, None)
        return dumps(output)


__all__ = ['DeviceConfiguration']
