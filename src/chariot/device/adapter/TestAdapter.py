from queue import Queue
from typing import Union
from random import random, seed
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.TestConfiguration import TestConfiguration
from chariot.utility.JSONTypes import JSONObject
from chariot.utility.ChariotExceptions import *


class TestAdapter(DeviceAdapter):
    def __init__(self, config: TestConfiguration):
        super().__init__(config)

    def _beginDataCollection(self, errorQueue: Queue) -> None:
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
        bufSize = self._conifg.buffSize
        while self.inCollectionEpisode:
            buf: List[float] = [0 for _ in bufSize]
            for i in range(bufSize):
                buf[i] = random()
            self.dataQueue.put(buf, block=True)

__all__ = ['TestAdapter']
