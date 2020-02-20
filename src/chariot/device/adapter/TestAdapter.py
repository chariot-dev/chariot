from queue import Queue
from typing import Union
from random import random, seed
from chariot.JSONTypes import JSONObject
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.TestConfiguration import TestConfiguration
from chariot.utility.ChariotExceptions import *

class TestAdapter(DeviceAdapter):
    def __init__(self, config: TestConfiguration):
        super().__init__(config)

    def beginDataCollection(self, errorQueue: Queue) -> None:
        if not self.connected:
            stackTrace = self._generateStackTrace(DeviceNotConnectedError())
            errorQueue.put(stackTrace, block=True)
        self.inCollectionEpisode = True
        self. randomizer()

    def connect(self) -> None:
       self.connected = True

    def disconnect(self) ->None:
        self.connected = False

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