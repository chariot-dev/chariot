from abc import ABCMeta, abstractmethod
from sys import exc_info
from time import time
from typing import Dict, Type
from queue import SimpleQueue as Queue
from chariot.device.configuration import DeviceConfiguration
from chariot.utility.exceptions.ChariotExceptions import *
from chariot.utility.JSONTypes import JSONObject

class DeviceAdapter(metaclass=ABCMeta):
    def __init__(self, config: Type[DeviceConfiguration]):
        self._config: Type[DeviceConfiguration] = config
        self.connected: bool = False
        self.dataQueue: Queue = Queue()
        self.inCollectionEpisode = False

    # this method should only be run as the target of a ProducerThread
    def startDataCollection(self) -> None:
        if self.inCollectionEpisode:
            return
        if not self.connected:
            self.connect()
        self.inCollectionEpisode = True
        self._startDataCollection()

    @abstractmethod
    def _startDataCollection(self) -> None:
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
            raise DeviceNotConnectedError()
        self._disconnect()
        self.connected = False

    @abstractmethod
    def _disconnect(self) -> None:
        pass

    def getConfiguration(self) -> DeviceConfiguration:
        return self._config

    def getDataQueue(self) -> Queue:
        return self.dataQueue

    def getDeviceType(self) -> str:
        return self._config.deviceType

    def getId(self) -> str:
        return self._config.deviceId

    def setId(self, newId) -> str:
        self._config.deviceId = newId

    def _reportData(self, data: Dict[str, JSONObject]):
        self.dataQueue.put({
            'device_name': self._config.deviceId,
            'production_time': int(round(time() * 1000)),
            'freeform': data,
            })

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


__all__ = ['DeviceAdapter']
