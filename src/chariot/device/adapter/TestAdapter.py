from queue import Queue
from typing import List, Union
from time import sleep, time
from random import random, seed
from chariot.device.adapter import DeviceAdapter
from chariot.device.configuration import TestConfiguration
from chariot.utility.JSONTypes import JSONObject
from chariot.utility.exceptions.ChariotExceptions import *


class TestAdapter(DeviceAdapter):
    def __init__(self, config: TestConfiguration):
        super().__init__(config)

    def _startDataCollection(self) -> None:
        self._inCollectionEpisode = True
        self._randomizer()

    # For testing purpose do things to mess up these functions and cause errors
    def _connect(self) -> None:
        pass

    def _disconnect(self) -> None:
        pass

    def _stopDataCollection(self) -> None:
        pass

    def _randomizer(self) -> None:
        seedVal = self._config.seedVal
        if seedVal == 0:
            seed()
        else:
            seed(seedVal)
        bufSize = self._config.buffSize
        while self.inCollectionEpisode:
            sleep(0.5)
            buf: List[float] = [random() for _ in range(bufSize)]
            self.dataQueue.put({'production_time': int(round(time() * 1000)), 'freeform': buf}, block=True)

__all__ = ['TestAdapter']
