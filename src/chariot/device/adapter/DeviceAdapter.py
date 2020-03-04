from abc import ABCMeta, abstractmethod
from sys import exc_info
from typing import Type
from queue import Queue
from chariot.utility.JSONTypes import JSONObject
from chariot.device.configuration import DeviceConfiguration

class DeviceAdapter(metaclass=ABCMeta):
    def __init__(self, config: Type[DeviceConfiguration]):
        self._config: Type[DeviceConfiguration] = config
        self.connected: bool = False
        self.dataQueue: Queue = Queue()
        self.inCollectionEpisode = False

    # this method should only be run as the target of a ProducerThread
    @abstractmethod
    def beginDataCollection(self, errorQueue: Queue) -> None:
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
        return self._config.deviceType

    def getId(self) -> str:
        return self._config.deviceId

    def setId(self, newId) -> str:
        self._config.deviceId = newId

    # https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
    # "hack" to generate the entire stack trace since beginDataCollection is called in a different thread
    # might add the thread's name explicitly so the DataCollectionManager knows which device produced the error
    def _generateStackTrace(self, error: Exception):
        try:
            raise error
        except Exception:
            return exc_info()

    def stopDataCollection(self) -> None:
        self.inCollectionEpisode = False

    def getDeviceConfiguration(self) -> Type[DeviceConfiguration]:
        return self._config

    def setDeviceConfiguration(self, config: Type[DeviceConfiguration]) -> None:
        self._config = config

__all__ = ['DeviceAdapter']
