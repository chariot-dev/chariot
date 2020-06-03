from multiprocessing import Event, Process, RLock, Queue
from typing import Callable, Dict, List, Optional
from queue import Empty
from chariot.device import DeviceAdapterFactory, DeviceConfigurationFactory
from chariot.device.adapter import DeviceAdapter
from chariot.device.configuration import DeviceConfiguration
from chariot.configuration import Configuration
from chariot.database.configuration import DatabaseConfiguration
from chariot.database import DatabaseConfigurationFactory, DatabaseWriterFactory
from chariot.database.writer import DatabaseWriter
from chariot.network import Network
from chariot.network.configuration import NetworkConfiguration
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.collection import DataCollector
from chariot.utility.JSONTypes import JSONObject
from test.testutils import MockServer


# this only works when the server is running in development mode
# it is a hack and is quite inefficient
# a more robust solution using Celery and an MQ service should be considered
class DataCollectionRunner:
    DEFAULT_TIMEOUT: float = 3600.0 

    def __init__(self):
        self._running: bool = False
        self._instance: Optional[DataCollector] = None
        self._runLock: RLock = RLock()
        self._stopEvent: Event = Event()
        self._taskQueue: Queue = Queue()
        self._process: Optional[Process] = None

    # this runs in a subprocess and since items cannot be pickled for various reasons,
    # it remakes all the objects needed and runs collection
    def _taskLoop(self, event: Event):
        while True:
            try:
                task: Optional[DataCollector] = self._taskQueue.get(block=True, timeout=self.DEFAULT_TIMEOUT)
                if task is None:
                    break

                networkConfig: JSONObject = {key: val for key, val in task['network'].items() 
                    if key in {'networkName', 'description'}}
                network: Network = Network(NetworkConfiguration(networkConfig))

                devices: List[JSONObject] = [val for key, val in task['network'].items() 
                    if key not in {'networkName', 'description'}]
                deviceConfigs: List[DeviceConfiguration] = [DeviceConfigurationFactory.getInstance(val) for val in devices]
                deviceList: List[DeviceAdapter] = [DeviceAdapterFactory.getInstance(val) for val in deviceConfigs]
                for device in deviceList:
                    network.addDevice(device)
                hasTestDevice: bool = any((device.getDeviceType() == 'TestDeviceAdapter' for device in deviceList))

                dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(task['database'])
                database: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)

                collectorConfig = task['collector']
                collectorConfig['network'] = network
                collectorConfig['database'] = database

                collector = DataCollector(DataCollectionConfiguration(collectorConfig))
                for hook in task['hooks']:
                    collector.addOutputHook(hook)
                collector.setErrorHandler(task['onEnd'])
                collector.setEndHandler(task['onError'])
                mockServer: Optional[MockServer] = None
                if hasTestDevice:
                    mockServer = MockServer()
                    mockServer.start()
                collector.startCollection()                
                event.wait()
                collector.stopCollection()
                if mockServer is not None:
                    mockServer.stop()
                event.clear()
            except Empty:
                continue

    def getCurrentInstance(self) -> Optional[DataCollector]:
        with self._runLock:
            return self._instance

    def isRunning(self) -> None:
        with self._runLock:
            return self._running

    def runTask(self, instance: DataCollector) -> None:
        with self._runLock:
            if self._running:
                raise AssertionError('An instance of data collection was already running.')

            if self._stopEvent.is_set():
                self._stopEvent.clear()
            self._instance = instance
            self._running = True
            task: Dict[str, JSONObject] = {}
            task['network'] = self._instance.getNetwork().toDict()
            task['database'] = self._instance.getDatabase().getConfiguration().toDict()
            task['collector'] = self._instance.getConfiguration().toDict().copy()
            del task['collector']['network']
            del task['collector']['database']
            task['hooks'] = self._instance._outputHooks
            task['onEnd'] = self._instance._onEnd
            task['onError'] = self._instance._onError
            self._taskQueue.put(task)

    def start(self) -> None:
        self._process = Process(target=self._taskLoop, args=(self._stopEvent,))
        self._process.start()

    def stop(self) -> None:
        with self._runLock:
            if self._running:
                self.stopTask()
            self._taskQueue.put(None)
            if self._process and self._process.is_alive():
                self._process.join()

    def stopTask(self) -> None:
        with self._runLock:
            if not self._running:
                raise AssertionError('No instance of data collection was running.')
            self._stopEvent.set()
            self._running = False
