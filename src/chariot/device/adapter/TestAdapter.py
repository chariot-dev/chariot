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
        self.randomizer()

    def _connect(self) -> None:
        pass

    def _disconnect(self) -> None:
        pass

    def randomizer(self) -> None:
        seedVal = self._config.seedVal
        if seedVal == 0:
            seed()
        else:
            seed(seedVal)
        bufSize = self._conifg.buffSize
        while self.inCollectionEpisode:
            buf = list()
            i = 0
            while i < bufSize:
                buf.append(random())
                i += 1
            self.dataQueue.put(buf)

__all__ = ['TestAdapter']
