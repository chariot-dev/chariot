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
        self._dataQueue: Queue = Queue()
        self._inCollectionEpisode: bool = False

    # this method should only be run as the target of a ProducerThread
    def startDataCollection(self) -> None:
        if self._inCollectionEpisode:
            return
        if not self.connected:
            self.connect()
        self._inCollectionEpisode = True
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
            return
        self._disconnect()
        self.connected = False

    @abstractmethod
    def _disconnect(self) -> None:
        pass

    def getConfiguration(self) -> DeviceConfiguration:
        return self._config

    def getDataQueue(self) -> Queue:
        return self._dataQueue

    def getDeviceType(self) -> str:
        return self._config.deviceType

    def getId(self) -> str:
        return self._config.deviceId

    def setId(self, newId) -> str:
        self._config.deviceId = newId

    def _reportData(self, data: Dict[str, JSONObject]):
        self._dataQueue.put({
            'device_name': self._config.deviceId,
            'production_time': int(round(time() * 1000)),
            'freeform': data,
            })

    def stopDataCollection(self) -> None:
        if not self._inCollectionEpisode:
            return
        self._stopDataCollection()
        self._inCollectionEpisode = False

    @abstractmethod
    def _stopDataCollection(self) -> None:
        pass

    def toDict(self) -> None:
        return self._config.toDict()

    def updateConfig(self, config: JSONObject) -> None:
        if self._inCollectionEpisode:
            raise AssertionError('Cannot modify device configuration during a collection episode')
        self._config.updateConfig(config)


__all__ = ['DeviceAdapter']
