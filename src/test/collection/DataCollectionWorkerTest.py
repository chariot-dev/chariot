import pytest
from multiprocessing import Event
from time import sleep
from threading import Thread
from typing import Dict, List, Optional
from queue import SimpleQueue as Queue
from chariot.collection import DataCollectionWorker
from chariot.utility.JSONTypes import JSONObject
from test.testutils import MockDeviceTester, MockServer, TestDeviceAdapter, TestDeviceConfiguration


class DataCollectionWorkerTest(MockDeviceTester):
    instance: Optional[DataCollectionWorker] = None
    NUM_DEVICES: int = 8
    EPISODE_LEN: float = 10.0
    dataStore: Queue = Queue()

    def _loadDevices(self):
        devices: List[TestDeviceAdapter] = []
        for i in range(self.NUM_DEVICES):
            devices.append(self._buildDevice(f'Test Device {i}', 200, i))
        self.instance = DataCollectionWorker(devices)
        self.instance.addOutputHook(self._outputData)

    def _outputData(self, data: JSONObject) -> None:
        self.dataStore.put(data)

    def emptyWorkerTest(self):
        self.instance = DataCollectionWorker([])
        with pytest.raises(AssertionError):
            self.instance.start(Event())

    def validEpisodeTest(self) -> None:
        self._loadDevices()
        stopEvent: Event = Event()
        self.instance.start(stopEvent)
        sleep(self.EPISODE_LEN)
        stopEvent.set()
        sleep(.5)
        assert self.instance.isRunning() == False

        # sentintel value to signal queue is empty
        self.dataStore.put(None)
        dataDict: Dict[str, List[JSONObject]] = {}
        for data in iter(self.dataStore.get, None):
            if not data[0]['device_name'] in dataDict:
                dataDict[data[0]['device_name']] = [chunk for chunk in data]
            else:
                dataDict[data[0]['device_name']].extend(data)

        # assert every device was able to report data
        assert len(dataDict.keys()) == self.NUM_DEVICES
