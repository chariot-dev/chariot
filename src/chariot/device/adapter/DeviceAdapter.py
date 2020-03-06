from abc import ABCMeta, abstractmethod
from sys import exc_info
from typing import Type
from queue import Queue
from chariot.utility.JSONTypes import JSONObject
from chariot.device.configuration import DeviceConfiguration
from chariot.utility.exceptions.ChariotExceptions import *

class DeviceAdapter(metaclass=ABCMeta):
    def __init__(self, config: Type[DeviceConfiguration]):
        self._config: Type[DeviceConfiguration] = config
        self.connected: bool = False
        self.dataQueue: Queue = Queue()
        self.inCollectionEpisode = False
        self.tmp = 0            #temporary counter delete from push

    # this method should only be run as the target of a ProducerThread
    def beginDataCollection(self) -> None:
        if not self.connected:
            raise DeviceNotConnectedError()
        if self.inCollectionEpisode:
            raise InCollectionEpisodeError()
        self.inCollectionEpisode = True

        if self.tmp == 1:
            self._beginDataCollection()
        else:
            self.tmp = 1
            self.inCollectionEpisode = False
            raise FailedToBeginCollectionError()

    @abstractmethod
    def _beginDataCollection(self) -> None:
        pass

    # any procedures necessary to start capturing data from the device
    def connect(self, reconnect=False) -> None:
       # if reconnect:
       #     self.tmp = 1
        if reconnect or not self.connected:
            self._connect()
           # if self.tmp == 0:
           #     self.connected = False
           # else:
            self.connected = True

    @abstractmethod
    def _connect(self) -> None:
        pass

    # gracefully close the connection to the device
    def disconnect(self) -> None:
        if not self.connected:
            raise DeviceNotConnectedError()
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

    def setId(self, newId) -> str:
        self._config.deviceId = newId

    def stopDataCollection(self) -> None:
        if not self.inCollectionEpisode:
            raise AssertionError
        self._stopDataCollection()
        self.inCollectionEpisode = False

    @abstractmethod
    def _stopDataCollection(self) -> None:
        pass

    def getDeviceConfiguration(self) -> Type[DeviceConfiguration]:
        return self._config

    def setDeviceConfiguration(self, config: Type[DeviceConfiguration]) -> None:
        self._config = config

__all__ = ['DeviceAdapter']
