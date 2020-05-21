import requests
from typing import List, Union
from time import sleep
from chariot.device.adapter import DeviceAdapter
from test.testutils import ErrorDeviceConfiguration
from chariot.utility.JSONTypes import JSONObject
from chariot.utility.exceptions.ChariotExceptions import *


class ErrorDeviceAdapter(DeviceAdapter):
    def __init__(self, config: ErrorDeviceConfiguration, error: int):
        super().__init__(config)
        self.errorToRun: int= error

    def _startDataCollection(self) -> None:
        errCnt: int = 0

        pollDelay = self._config.pollDelay / 1000
        while self._inCollectionEpisode:
            if not self.connected:
                raise AssertionError

            response: requests.Response = requests.get(f'http://localhost:{self._config.port}/data')
            data: JSONObject = response.json()
            self._reportData(data)
            sleep(pollDelay)

            if errCnt == 50:
                errCnt += 1
                self.deviceErrors(self.errorToRun)
            errCnt += 1

    def _connect(self) -> None:
        pass

    def _disconnect(self) -> None:
        pass

    def _stopDataCollection(self) -> None:
        pass
    
    def deviceErrors(self, type: int) -> None:
        if type == 1:
            raise DeviceNotConnectedError
        elif type == 2:
            raise NotInCollectionEpisodeError
        elif type == 3:
            raise FailedToBeginCollectionError
        elif type == 4:
            raise NotInCollectionEpisodeError
        else:
            return

__all__ = ['ErrorDeviceAdapter']