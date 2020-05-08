from math import ceil
from queue import Empty
from multiprocessing import cpu_count, Event
from multiprocessing import SimpleQueue as Queue
from sys import exc_info
from re import match
from threading import Lock, Timer
from time import sleep
from typing import Callable, Dict, Iterable, List, Optional
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.collection import DataCollectionWorker
from chariot.database.writer import DatabaseWriter
from chariot.device.adapter import DeviceAdapter
from chariot.network import Network
from chariot.utility.concurrency import HandledProcess, HandledThread
from chariot.utility.JSONTypes import JSONObject
from chariot.utility.exceptions import DeviceNotConnectedError, InCollectionEpisodeError, NotInCollectionEpisodeError, FailedToBeginCollectionError


class DataCollector:
    MAX_DEVICES_PER_WORKER: int = 8
    JOIN_TIMEOUT: float = 1.0
    PROCESS_CREATION_DELAY = 0.1

    def __init__(self, configuration: DataCollectionConfiguration, onEnd: Optional[Callable] = None, onError: Optional[Callable] = None):
        self._config: DataCollectionConfiguration = configuration
        self._devices: List[DeviceAdapter] = []
        self._errorHandler: HandledThread = HandledThread(name='Error-Handler', target=self._handleErrors)
        self._errorQueue: Queue = Queue()
        self._runLock = Lock()
        self._onEnd: Optional[Callable] = onEnd
        self._onError: Optional[Callable[Exception], None] = onError
        self._running: bool = False
        self._stopEvent: Event = Event()
        self._stopTimer: Optional[Timer] = None
        self._workers: List[DataCollectionWorker] = []
        self._workerProcesses: List[HandledProcess] = []
        self._minPollDelay: float = 0.01

    def __del__(self) -> None:
        self.stopCollection()

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

        MAX_ATTEMPTS: int = 3
        reconnects: Dict[DataCollectionWorker, Dict[DeviceAdapter, int]] = {}

        # Create dictionaries at start
        for worker in self._workers:
            reconnects[worker] = {}
            for device in worker._devices:
                reconnects[worker][device] = 0

        while self._running:
            for worker in self._workers:
                try:
                # Process: (Process Name, Error, Error output as a list of strings)
                # Thread: (Thread Name, Stack Trace)
                    name, err, tb = worker.getErrorQueue().get_nowait()

                    # Error Handling depends on what kind of Thread/Process we are dealing with
                    if match(r"Producer:*",name):
                        deviceID = name[10:]  

                        device: DeviceAdapter = None # Extract device adapter for direct access 
                        for dev in self._devices:
                            if dev.getId == deviceID:
                                device = dev


                        if err is DeviceNotConnectedError:        # Disconnected Device
                            if device in reconnects[worker]:
                                reconnects[worker][device] += 1
                            else:
                                reconnects[worker][device] = 1

                            if reconnects[worker][device] == MAX_ATTEMPTS:
                                self._onError(err)                          # Inform user Chariot can't automattically reconnect

                            elif reconnects[worker][device] > MAX_ATTEMPTS:
                                continue
                            else:
                                worker.addDeviceDuringDCE(device,True)
                        elif err is InCollectionEpisodeError:    # Tried to do something during DCE, may need extra info on the kind of operation
                            pass
                        elif err is NotInCollectionEpisodeError: # Tried to do something outside a DCE
                            pass
                        elif err is FailedToBeginCollectionError:
                            pass
                        else:
                            self._onError(err)      # assuming this is how _onError works
                        pass
                    elif match(r"DataCollectionWorker-*",name):
                        workerNum: int = int(name[21:]) - 1
                        
                        # Need to test for different kinds of errors first, for now just remake thread
                        self._restartWorker(workerNum)
                    else:                                            # Other, unchecked Error Generators
                        pass
                except Empty:
                    continue
                
        #   pass
        pass

    def isRunning(self) -> bool:
        return self._running

    def setErrorHandler(self, handler: Callable[[Exception], None]) -> None:
        if not callable(handler):
            raise AssertionError
        self._onError = handler

    # if it was a timed collection episode, execute this once it's done
    def setEndHandler(self, handler: Callable) -> None:
        if not callable(handler):
            raise AssertionError
        self._onEnd = handler

    def _restartWorker(self, workerNum: int) -> None:
        numDevices: int = len(self._devices)
        numWorkers: int = ceil(numDevice / self.MAX_DEVICES_PER_WORKER)
        avgDevicesPerWorker: int = int(round(numDevices / numWorkers))

        startIdx: int = avgDevicesPerWorker * workerNum
        endIdx: int = min(startIdx + avgDevicesPerWorker, numDevices)
        
        worker: DataCollectionWorker = DataCollectionWorker(self._devices[startIdx:endIdx], self._minPollDelay)
        worker.addOutputHook(self._config.database.insertMany)
        self._workers[workerNum] = worker

        workerProcess: HandledProcess = HandledProcess(
            target=worker.start, name=f'DataCollectionWorker-{(workerNum + 1)}', args=(self._errorQueue, self._stopEvent))

        self._workerProcesses[workerNum] = workerProcess

        workerProcess.start()


    def startCollection(self) -> None:
        if self._running:
            # not sure whether to raise an error here
            return

        network: Network = self._config.network
        self._devices = [device for device in network.getDevices().values()]
        if len(self._devices) == 0:
            raise AssertionError('Can\'t collect data from a network with no devices')
        
        # set the minimum poll delay for any action to the max between the default and 90% of the min from the devices in a network
        devicePolls: Iterable[DeviceAdapter] = (0.9 * device.getConfiguration().pollDelay / 1000 for device in self._devices)
        minDevicePoll: float = min(devicePolls)
        self._minPollDelay = max(self._minPollDelay, minDevicePoll)

        self._config.database.connect()

        numDevices = len(self._devices)
        numWorkers = ceil(numDevices / self.MAX_DEVICES_PER_WORKER)
        avgDevicesPerWorker: int = int(round(numDevices / numWorkers))

        # split devices as equally as possible among workers
        for i in range(0, numDevices, avgDevicesPerWorker):
            index: int = i // avgDevicesPerWorker
            startIdx: int = i
            endIdx: int = min(startIdx + avgDevicesPerWorker, numDevices)
            worker: DataCollectionWorker = DataCollectionWorker(self._devices[startIdx:endIdx], self._minPollDelay)
            # output hooks are called when data is received and chunked - this is where we would add the socket.send
            # for the DataOutputAdapter
            worker.addOutputHook(self._config.database.insertMany)
            self._workers.append(worker)
            workerProcess: HandledProcess = HandledProcess(
                target=worker.start, name=f'DataCollectionWorker-{(index + 1)}', args=(self._errorQueue, self._stopEvent))
            self._workerProcesses.append(workerProcess)

        self._running = True
        self._runLock.acquire()
        network.lock(self._runLock, 'a data collection episode')
        self._config.database.lock(self._runLock, 'a data collection episode')
        self._errorHandler.start()
        for workerProcess in self._workerProcesses:
            workerProcess.start()
            sleep(self.PROCESS_CREATION_DELAY) # seems to be necessary to avoid random bad forks
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
        self._runLock.release()

        if not calledFromTimer and self._stopTimer:
            if self._stopTimer.is_alive():
                self._stopTimer.cancel()
                # not sure if cancel calls join, i.e. if it's necessary to join on a Timer
                # Timer source: https://github.com/python/cpython/blob/dab8423d220243efabbbcafafc12d90145539b50/Lib/threading.py#L1249
                self._stopTimer.join()
                self._stopTimer = None
        if self._onEnd:
            self._onEnd()

    def stopCollection(self, *args) -> None:
        return self._stopCollection(False)

    def updateConfig(self, config: JSONObject) -> None:
        if self._running:
            raise AssertionError('Cannot modify a data collection configuration during a data collection episode')
        self._config.updateConfig(config)
