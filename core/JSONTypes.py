from typing import Dict, List, Union

# workaround for recursive types with mypy: https://gist.github.com/catb0t/bd82f7815b7e95b5dd3c3ad294f3cbbf
# modified from original source: https://github.com/python/mypy/issues/731#issuecomment-539905783

JSONValue = Union[str, int, float, bool, None]
JSONObject = Union[JSONValue, 'JSONDict', 'JSONList']

class JSONDict(Dict[str, JSONObject]):
    pass

class JSONList(List[JSONObject]):
    pass
    
__all__ = ['JSONDict', 'JSONList', 'JSONObject', 'JSONValue']
