from math import ceil
from multiprocessing import Event, Queue
from threading import Timer
from time import sleep
from typing import Callable, Iterable, List, Optional, Set
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.collection import DataCollectionWorker
from chariot.database import DatabaseConfigurationFactory
from chariot.database.writer import DatabaseWriter
from chariot.device.adapter import DeviceAdapter
from chariot.network import Network
from chariot.utility.concurrency import HandledProcess, HandledThread
from chariot.utility.JSONTypes import JSONObject


class DataCollector:
    MAX_DEVICES_PER_WORKER: int = 8
    JOIN_TIMEOUT: float = 1.0
    PROCESS_CREATION_DELAY = 0.1

    def __init__(self, configuration: DataCollectionConfiguration, onEnd: Optional[Callable] = None,
                 onError: Optional[Callable] = None):
        self._config: DataCollectionConfiguration = configuration
        self._devices: List[DeviceAdapter] = []
        self._errorHandler: HandledThread = HandledThread(name='Error-Handler', target=self._handleErrors)
        self._errorQueue: Queue = Queue()
        self._onEnd: Optional[Callable] = onEnd
        self._onError: Optional[Callable[Exception], None] = onError
        # this should be a set, but causes issues in < v3.8: 
        # https://stackoverflow.com/questions/13264511/typeerror-unhashable-type-dict
        self._outputHooks: List[Callable] = [] 
        self._running: bool = False
        self._stopEvent: Event = Event()
        self._stopTimer: Optional[Timer] = None
        self._workers: List[DataCollectionWorker] = []
        self._workerProcesses: List[HandledProcess] = []
        self._minPollDelay: float = 0.01

    # output hooks cannot be added during a collection episode
    def addOutputHook(self, hook: Callable) -> None:
        if not callable(hook):
            raise AssertionError
        self._outputHooks.append(hook)

    def clearOutputHooks(self) -> None:
        self._outputHooks.clear()

    def getConfiguration(self) -> DataCollectionConfiguration:
        return self._config

    def getDatabase(self) -> DatabaseWriter:
        return self._config.database

    def getId(self) -> str:
        return self._config.configId

    def getNetwork(self) -> Network:
        return self._config.network

    # implement error handling using self._errorQueue here, this runs in a separate thread
    def _handleErrors(self) -> None:
        # use self._onError to report errors that cannot be handled here and should be passed to the user
        # the API should pass in an errorhandler method as onError
        # go through each worker and do worker.getErrorQueue().get_nowait()
        # while self._running:
        #   pass
        pass

    def isRunning(self) -> bool:
        return self._running

    # output hooks cannot be removed during a collection episode
    def removeOutputHook(self, hook: Callable) -> None:
        self._outputHooks.remove(hook)

    def setErrorHandler(self, handler: Optional[Callable]) -> None:
        if handler is not None and not callable(handler):
            raise AssertionError
        self._onError = handler

    # if it was a timed collection episode, execute this once it's done
    def setEndHandler(self, handler: Optional[Callable]) -> None:
        if handler is not None and not callable(handler):
            raise AssertionError
        self._onEnd = handler

    def startCollection(self) -> None:
        if self._running:
            # not sure whether to raise an error here
            return
        if self._stopEvent.is_set():
            self._stopEvent.clear()
        network: Network = self._config.network
        self._devices = [device for device in network.getDevices().values()]
        if len(self._devices) == 0:
            raise AssertionError('Can\'t collect data from a network with no devices')

        # set the minimum poll delay for any action to the max between
        # the default and 90% of the min from the devices in a network
        devicePolls: Iterable[DeviceAdapter] = (0.9 * device.getConfiguration().pollDelay / 1000 for device in self._devices)
        minDevicePoll: float = min(devicePolls)
        self._minPollDelay = max(self._minPollDelay, minDevicePoll)

        numDevices = len(self._devices)
        numWorkers = ceil(numDevices / self.MAX_DEVICES_PER_WORKER)
        avgDevicesPerWorker: int = int(round(numDevices / numWorkers))

        # split devices as equally as possible among workers
        for i in range(0, numDevices, avgDevicesPerWorker):
            startIdx: int = i
            endIdx: int = min(startIdx + avgDevicesPerWorker, numDevices)
            
            worker: DataCollectionWorker = None
            if self._config.database.__class__.__name__ == 'TestDatabaseWriter':
                worker = DataCollectionWorker(self._devices[startIdx:endIdx])
                self._config.database.connect()
                worker.addOutputHook(self._config.database.insertMany)
            else:
                worker = DataCollectionWorker(self._devices[startIdx:endIdx],
                    DatabaseConfigurationFactory.getInstance(self._config.database.getConfiguration().toDict()), self._minPollDelay)
            for hook in self._outputHooks:
                worker.addOutputHook(hook)

            self._workers.append(worker)
            workerProcess: HandledProcess = HandledProcess(
                target=worker.start, name=f'DataCollectionWorker-{(i//8 + 1)}', args=(self._errorQueue, self._stopEvent))
            self._workerProcesses.append(workerProcess)

        self._running = True
        self._errorHandler.start()

        for workerProcess in self._workerProcesses:
            workerProcess.start()

        if hasattr(self._config, 'runTime'):
            self._stopTimer = Timer(float(self._config.runTime / 1000), self._stopCollection, args=(True,))
            self._stopTimer.start()

    def _stopCollection(self, calledFromTimer: bool = False) -> None:
        if not self._running:
            return

        self._running = False
        # each worker waits for this event to be set, and then stops
        self._stopEvent.set()
        alive: bool = True
        while alive:
            alive = False
            for workerProcess in self._workerProcesses:
                workerProcess.join(self.JOIN_TIMEOUT)
                alive |= workerProcess.is_alive()
            self._errorHandler.join(self.JOIN_TIMEOUT)
            alive |= self._errorHandler.is_alive()
        self._config.database.disconnect()
        self._workerProcesses.clear()
        self._workers.clear()
        self._devices.clear()

        if not calledFromTimer and self._stopTimer:
            if self._stopTimer.is_alive():
                self._stopTimer.cancel()
                # not sure if cancel calls join, i.e. if it's necessary to join on a Timer. Timer Source:
                # https://github.com/python/cpython/blob/dab8423d220243efabbbcafafc12d90145539b50/Lib/threading.py#L1249
                self._stopTimer.join()
                self._stopTimer = None
        if self._onEnd:
            self._onEnd()

    def stopCollection(self, *args) -> None:
        return self._stopCollection(*args)

    def updateConfig(self, config: JSONObject) -> None:
        if self._running:
            raise AssertionError('Cannot modify a data collection configuration during a data collection episode')
        self._config.updateConfig(config)
