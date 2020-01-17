from typing import Any, Dict, Union
from .DeviceConfiguration import DeviceConfiguration

class DeviceAdapter:
    def __init__(self, _id: str, name: str, config: DeviceConfiguration):
        self.id: str = _id
        self.name: str = name
        self.nickname: str = str()
        self.unpackConfig(config)

     # get a packet of data from the device 
    def captureData(self) -> Dict[str, Union[str, Dict[str, Any]]]:
        pass

    # gracefully close the connection to the device
    def cleanup(self) -> None:
        pass

    # any procedures necessary to start capturing data from the device
    def initialize(self) -> None:
        pass

    # all fields the class requires should be guaranteed to exist, so we set them without error checking
    # for optional fields, they are set as None if not set
    def unpackConfig(self, config: DeviceConfiguration) -> None:
        self.nickname = config.nickname


__all__ = ['DeviceAdapter']