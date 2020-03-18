from math import ceil
from multiprocessing import cpu_count, Process
from multiprocessing.queues import SimpleQueue as Queue
from queue import Empty as QueueEmptyException
from threading import Timer
from typing import Callable, List, Optional
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.collection import DataCollectionWorker
from chariot.database.writer import DatabaseWriter
from chariot.device.adapter import DeviceAdapter
from chariot.network import Network
from chariot.utility.concurrency import HandledProcess, HandledThread


class DataCollector:
    MAX_DEVICES_PER_WORKER: int = 8
    THREAD_JOIN_TIMEOUT: float = 2.0

    def __init__(self, configuration: DataCollectionConfiguration, onEnd: Optional[Callable] = None, onError: Optional[Callable] = None):
        self._config: DataCollectionConfiguration = configuration
        self._devices: List[DeviceAdapter] = []
        self._errorHandler: HandledThread = HandledThread(name='Error-Handler', target=self._handleErrors)
        self._errorQueue: Queue = Queue()
        self._onEnd: Optional[Callable] = onEnd
        self._onError: Optional[Callable[Exception], None] = onError
        self._running: bool = False
        self._stopTimer: Optional[Timer] = None
        self._workers: List[DataCollectionWorker] = []
        self._workerProcesses: List[HandledProcess] = []

    # implement error handling using self._errorQueue here, this runs in a separate thread
    def _handleErrors(self) -> None:
        # use self._onError to report errors that cannot be handled here and should be passed to the user
        # the API should pass in an errorhandler method as onError
        while self._running:
            pass

    def _stopCollection(self, calledFromTimer: bool = False) -> None:
        if not self._running:
            return
        
        self._running = False
        alive: bool = True
        while alive:
            alive = False
            for worker in self._workers:
                worker.stop()
                alive |= worker.isRunning()
            for workerProcess in self._workerProcesses:
                workerProcess.join(self.THREAD_JOIN_TIMEOUT)
                alive |= workerProcess.is_alive()
            self._errorHandler.join(self.THREAD_JOIN_TIMEOUT)
            alive |= self._errorHandler.is_alive()
        self._config.database.disconnect()
        self._workerProcesses.clear()
        self._workers.clear()
        self._devices.clear()

        if not calledFromTimer and self._stopTimer:
            if self._stopTimer.is_alive():
                self._stopTimer.cancel()
                # not sure if cancel calls join, i.e. if it's necessary to join on a Timer
                # Timer source: https://github.com/python/cpython/blob/dab8423d220243efabbbcafafc12d90145539b50/Lib/threading.py#L1249
                self._stopTimer.join()
                self._stopTimer = None
        if self._onEnd:
            self._onEnd()

    def getConfiguration(self) -> DataCollectionConfiguration:
        return self._config

    def getDatabase(self) -> DatabaseWriter:
        return self._config.database

    def getNetwork(self) -> Network:
        return self._config.network

    def setErrorHandler(self, handler: Callable[[Exception], None]) -> None:
        if not callable(handler):
            raise AssertionError
        self._onError = handler

    def setEndHandler(self, handler: Callable) -> None:
        if not callable(handler):
            raise AssertionError
        self._onEnd = handler

    def startCollection(self) -> None:
        if self._running:
            # not sure whether to raise an error here
            return

        network: Network = self._config.network
        self._devices = [device for device in network.getDevices().values()]
        if len(self._devices) == 0:
            raise AssertionError('Can\'t collect data from a network with no devices')

        dbWriter: DatabaseWriter = self._config.database
        dbWriter.connect()

        numDevices = len(self._devices)
        numWorkers = ceil(numDevices / self.MAX_DEVICES_PER_WORKER)
        avgDevicesPerWorker: int = int(round(numDevices / numWorkers))

        # split devices as equally as possible among workers
        for i in range(0, numDevices, avgDevicesPerWorker):
            startIdx: int = i
            endIdx: int = min(startIdx + avgDevicesPerWorker - 1, numDevices - 1)
            worker: DataCollectionWorker = DataCollectionWorker(self._devices[startIdx:endIdx])
            # output hooks are called when data is received and chunked - this is where we would add the socket.send 
            # for the DataOutputAdapter
            worker.addOutputHook(dbWriter.insertMany)
            self._workers.append(worker)
            workerProcess: HandledProcess = HandledProcess(
                target=worker.start, name=f'DataCollectionWorker-{i/8 + 1}', args=(self._errorQueue,))
            self._workerProcesses.append(workerProcess)

        self._errorHandler.start()
        for workerProcess in self._workerProcesses:
            workerProcess.start()
        if hasattr(self._config, 'runTime'):
            self._stopTimer = Timer(float(self._config.runTime / 1000), self._stopCollection, args=(True,))
            self._stopTimer.start()

    def stopCollection(self) -> None:
        return self._stopCollection(False)

    def updateConfig(self, config: JSONObject) -> None:
        if self._running:
            raise AssertionError
        self._config.updateConfig(config)
