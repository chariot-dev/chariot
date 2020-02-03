from abc import ABCMeta, abstractmethod
from sys import exc_info
from typing import Type
from queue import Queue
from core.JSONTypes import JSONDict, JSONObject
from core.device.configuration.DeviceConfiguration import DeviceConfiguration

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

    def getDataQueue(self) -> Queue:
        return self.dataQueue
    
    def getDeviceType(self) -> str:
        return self._config.deviceType

    def getId(self) -> str:
        return self._config.deviceId

    # https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
    # "hack" to generate the entire stack trace since beginDataCollection is called in a different thread
    # might add the thread's name explicitly so the DataCollectionManager knows which device produced the error
    def _generateStackTrace(error: Exception):
        try:
            raise error
        except Exception:
            return exc_info()

    def stopDataCollection(self) -> None:
        self.inCollectionEpisode = False


__all__ = ['DeviceAdapter']
