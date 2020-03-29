import requests
from typing import List, Union
from time import sleep
from chariot.device.adapter import DeviceAdapter
from test.testutils import TestDeviceConfiguration
from chariot.utility.JSONTypes import JSONObject
from chariot.utility.exceptions.ChariotExceptions import *


class TestDeviceAdapter(DeviceAdapter):
    def __init__(self, config: TestDeviceConfiguration):
        super().__init__(config)

    def _startDataCollection(self) -> None:
        pollDelay = self._config.pollDelay / 1000
        while self._inCollectionEpisode:
            if not self.connected:
                raise AssertionError

            response: requests.Response = requests.get('http://localhost:6000/data')
            data: JSONObject = response.json()
            self._reportData(data)
            sleep(pollDelay)

    def _connect(self) -> None:
        pass

    def _disconnect(self) -> None:
        pass

    def _stopDataCollection(self) -> None:
        pass

__all__ = ['TestDeviceAdapter']
