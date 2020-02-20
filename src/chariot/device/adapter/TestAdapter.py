from queue import Queue
from typing import Union
from random import rand
from chariot.JSONTypes import JSONObject
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.TestConfiguration import TestConfiguration
from chariot.utility.ChariotExceptions import *

class TestAdapter(DeviceAdapter):
    def __init__(self, config: TestConfiguration):
        super().__init__(config)

    def _beginDataCollection(self, errorQueue: Queue) -> None:
        pass

    def _connect(self) -> None:
        pass

    def _disconnect(self) ->None:
        pass