from abc import ABCMeta, abstractmethod
from sys import exc_info
from typing import Type
from queue import Queue
from chariot.JSONTypes import JSONObject
from chariot.device.configuration.DeviceConfiguration import DeviceConfiguration
from chariot.utility import ChariotExceptions

class DeviceAdapter(metaclass=ABCMeta):
    def __init__(self, config: Type[DeviceConfiguration]):
        self._config: Type[DeviceConfiguration] = config
        self.connected: bool = False
        self.dataQueue: Queue = Queue()
        self.inCollectionEpisode = False

    # this method should only be run as the target of a ProducerThread
    def beginDataCollection(self, errorQueue: Queue) -> None:
        if self.inCollectionEpisode:
            raise AssertionError
        self.inCollectionEpisode = True
        self._beginDataCollection(errorQueue)

    @abstractmethod
    def _beginDataCollection(self, errorQueue: Queue) -> None:
        pass

    # any procedures necessary to start capturing data from the device
    def connect(self, reconnect=False) -> None:
        if reconnect or not self.connected:
            self._connect()
            self.connected = True

    @abstractmethod
    def _connect(self) -> None:
        pass

    # gracefully close the connection to the device
    def disconnect(self) -> None:
        if not self.connected:
            raise AssertionError
        self._disconnect()
        self.connected = False

    @abstractmethod
    def _disconnect(self) -> None:
        pass

    def getDataQueue(self) -> Queue:
        return self.dataQueue

    def getDeviceType(self) -> str:
        return self._config.deviceType

    def getId(self) -> str:
        return self._config.deviceId

    def stopDataCollection(self) -> None:
        if not self.inCollectionEpisode:
            raise AssertionError
        self._stopDataCollection()
        self.inCollectionEpisode = False

    def _stopDataCollection(self) -> None:
        pass


__all__ = ['DeviceAdapter']
