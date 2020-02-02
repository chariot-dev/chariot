from abc import ABCMeta, abstractmethod
from typing import Type

from chariot.JSONTypes import JSONObject
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration


class DeviceAdapter(metaclass=ABCMeta):
    def __init__(self, config: Type[DeviceConfiguration]):
        self.config: Type[DeviceConfiguration] = config
        self.connected = False

    # get a packet of data from the device
    @abstractmethod
    def captureData(self) -> JSONObject:
        pass

    # any procedures necessary to start capturing data from the device
    @abstractmethod
    def connect(self) -> None:
        pass

    # gracefully close the connection to the device
    @abstractmethod
    def disconnect(self) -> None:
        pass

    def getDeviceType(self) -> str:
        return self.config.deviceType

    def getId(self) -> str:
        return self.config.deviceId

    def getNickname(self) -> str:
        return self.config.nickname


__all__ = ['DeviceAdapter']
