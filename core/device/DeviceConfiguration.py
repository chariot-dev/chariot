from typing import Dict, List
from json import dumps

class DeviceConfiguration:
    def __init__(self, configMap: Dict[str, Any]):
        self._required_fields: List[str] = ['nickname']
        self._optional_fields: List[str] = []
        
        for field in self._required_fields:
            try:
                setattr(self, field, configMap[field])
            except: 
                # handle error for missing required configuration
                pass

        for field in self._optional_fields:
                value = configMap[field] if field in configMap else None
                setattr(self, field, value)

    def __str__(self) -> str:
        output: Dict[str, str] = dict()
        # can probably make this more pythonian by using dict comprehension
        # but this is more convenient for debugging
        for field in self._required_fields:
            output[field] = getattr(self, field, None)
        for field in self._optional_fields:
            output[field] = getattr(self, field, None)
        return dumps(output)
