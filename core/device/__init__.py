from typing import Dict, List, Union

# workaround for recursive types with mypy: https://gist.github.com/catb0t/bd82f7815b7e95b5dd3c3ad294f3cbbf
# modified from original source: https://github.com/python/mypy/issues/731#issuecomment-539905783

ConfigValue = Union[str, int, float, bool, None]
ConfigObject = Union[ConfigValue, 'ConfigDict', 'ConfigList']

class ConfigDict(Dict[str, ConfigObject]):
    pass

class ConfigList(List[ConfigObject]):
    pass
