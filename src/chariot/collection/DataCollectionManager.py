from threading import Thread
# unused right now, but will be useful for scaling past a couple of devices
from multiprocessing.queues import Queue as ProcessQueue
from typing import List, Dict, Optional, Type
from sys import exc_info
from time import time
from queue import Empty as QueueEmptyException, Queue as ThreadQueue
from chariot.device.adapter import DeviceAdapter
from chariot.utility.JSONTypes import JSONObject
from chariot.network import Network
from chariot.database.writer import DatabaseWriter
from chariot.utility.exceptions.ChariotExceptions import *


class WorkerThread(Thread):
    def run(self):
        try:
            if self._target:
                self._target(*self._args[1:], **self._kwargs)
        except Exception as err:
            # add the error to the errorQueue for handling on the main thread
            # args[0]: the errorQueue passed in
#            self._args[0].put((self.name, exc_info()))
            self._args[0].put((self.name, err))
        finally:
            # https://github.com/python/cpython/blob/9c87fbe54e1c797e3c690c6426bdf5e79c457cf1/Lib/threading.py#L872
            del self._target, self._args, self._kwargs


class DataCollectionManager:
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network
    DEFAULT_TIMEOUT: float = 5.0
    ERROR_CHECK_TIMEOUT: float = 0.5
    PRODUCERS_PER_CONSUMER: int = 2
    THREAD_JOIN_TIMEOUT: float = 2.0

    # TODO: add __del__ method to stop data collection when this object goes out of scope
    # TODO: add DataOutputStream for outputThread to also send data to
    def __init__(self, network: Optional[Network], dbWriter: DatabaseWriter):
        self.activeNetwork: Optional[Network] = network
        self.devices: List[DeviceAdapter] = [
            device for _, device in network.getDevices().items()] if network is not None else []
        self.consumerThreads: List[WorkerThread] = []
        self.producerThreads: Dict[str, WorkerThread] = {}
        self.errorQueue: ThreadQueue = ThreadQueue()
        self.dataQueue: ThreadQueue = ThreadQueue()
        self.databaseWriter: DatabaseWriter = dbWriter
        self._inCollectionEpisode: bool = False
        self._episodeStartTime: int = 0
        self.outputThread: WorkerThread = WorkerThread(
            name='Output-Handler', target=self._outputData, args=(self.errorQueue,))

    def _consumeDataFromDevice(self, deviceIdx: int) -> None:
        device: DeviceAdapter = self.devices[deviceIdx]
        while self._inCollectionEpisode:
            output: List[JSONObject] = []
            try:
                data: JSONObject = device.getDataQueue().get(
                    block=True, timeout=self.DEFAULT_TIMEOUT)
                output.append(data)
            except QueueEmptyException:
                pass

            while True:
                try:
                    data: JSONObject = device.getDataQueue().get_nowait()
                    output.append(data)
                except QueueEmptyException:
                    break
            self.dataQueue.put(output, block=True)

    def _consumeDataFromDevices(self, startIdx: int, numDevices: int) -> None:
        if numDevices == 1:
            self._consumeDataFromDevice(startIdx)
        else:
            while self._inCollectionEpisode:
                output: List[JSONObject] = []
                for i in range(startIdx, startIdx + numDevices):
                    try:
                        data: JSONObject = self.devices[i].getDataQueue(
                        ).get_nowait()
                        output.append(data)
                    except QueueEmptyException:
                        continue
                if len(output) > 0:
                    self.dataQueue.put(output, block=True)

    def _handleErrorsInQueue(self) -> None:
        MAX_ATTEMPTS: int = 3
        disconnectedDevices: Dict[str, int] = {}
        failedCollections: Dict[str, int] = {}

        while self._inCollectionEpisode:
            try:
                # Errors received are a tuple of the Thread name/id and the stacktrace
                threadName, error = self.errorQueue.get(block=True, timeout=self.ERROR_CHECK_TIMEOUT)
                print(f'{threadName}: {error}')         #for testing
                if threadName == 'Output-Handler':
                    continue
                deviceID = threadName.strip('Producer-')

                errorDevice: DeviceAdapter = self.activeNetwork.getDeviceByDeviceName(deviceID)
                if isinstance(error, DeviceNotConnectedError):
                    if deviceID in disconnectedDevices:
                        if disconnectedDevices[deviceID] >= MAX_ATTEMPTS:
                            print(f'{deviceID} could not reconnect. Terminating device\'s data collection')     #for testing
#   Currently will cause issues with self.stopDataCollection if the device is stopped now, need to safely remove from local dicts, and lists
#                            errorDevice.stopDataCollection()
#                            del self.producerThreads[deviceID]


                        else:
                            disconnectedDevices[deviceID] += 1
                            errorDevice.connect(True)
                            producer = WorkerThread(
                                name=threadName, target=errorDevice.beginDataCollection, args=(self.errorQueue,))
                            self.producerThreads[deviceID] = producer
                            producer.start()

                    else:
                        disconnectedDevices[deviceID] = 0
                        errorDevice.connect(True)
                        producer = WorkerThread(
                            name=threadName, target=errorDevice.beginDataCollection, args=(self.errorQueue,))
                        self.producerThreads[deviceID] = producer
                        producer.start()
                elif isinstance(error, FailedToBeginCollectionError):
                    if deviceID in failedCollections:
                        if failedCollections[deviceID] >= MAX_ATTEMPTS:
                            print(f'{deviceID} failed to start collection after {MAX_ATTEMPTS} attemts.')
                        else:
                            print(f'{deviceID} attempting to restart data collection. Attempt: {failedCollections[deviceID]}')
                            failedCollections[deviceID] += 1
                            producer = WorkerThread(
                                name=threadName, target=errorDevice.beginDataCollection, args=(self.errorQueue,))
                            self.producerThreads[deviceID] = producer
                            producer.start()
                    else:
                        failedCollections[deviceID] = 0
                        print(f'{deviceID} attempting to restart data collection.')
                        producer = WorkerThread(
                            name=threadName, target=errorDevice.beginDataCollection, args=(self.errorQueue,))
                        self.producerThreads[deviceID] = producer
                        producer.start()
                else:
                    print(f'{deviceID} has encountered an unknown error')
                    errorDevice.inCollectionEpisode = False

            except QueueEmptyException:
                continue

    def _outputData(self) -> None:
        while self._inCollectionEpisode:
            output: List[JSONObject] = []
            try:
                data: JSONObject = self.dataQueue.get(
                    block=True, timeout=self.DEFAULT_TIMEOUT)
                for dataPoint in data:
                    dataPoint['relative_time'] -= self._episodeStartTime
                output.append(data)
            except QueueEmptyException:
                pass

            while True:
                try:
                    data = self.dataQueue.get_nowait()
                    # maybe verify at this point as well that the data format is correct?
                    for dataPoint in data:
                        dataPoint['relative_time'] -= self._episodeStartTime
                    output.append(data)
                except QueueEmptyException:
                    break
            for chunk in output:
                self.databaseWriter.insertMany(chunk)

    def inCollectionEpisode(self) -> bool:
        return self._inCollectionEpisode

    def setActiveNetwork(self, network: Optional[Network]):
        if self._inCollectionEpisode:
            raise InCollectionEpisodeError()
        self.activeNetwork = network
        if self.activeNetwork is not None:
            self.devices = [device for _, device in network.getDevices().items()]
        else:
            self.devices = []

    def getActiveNetwork(self) -> Optional[Network]:
        return self.activeNetwork

    def beginDataCollection(self) -> None:
        if self._inCollectionEpisode:
            raise InCollectionEpisodeError()

        self.databaseWriter.connect()
        self._episodeStartTime = int(round(time() * 1000))

        if len(self.devices) == 0:
            raise AssertionError(
                'Must have at least one device to collect from.')
        for device in self.devices:
            producer = WorkerThread(
                name=f'Producer-{device.getId()}', target=device.beginDataCollection, args=(self.errorQueue,))
            self.producerThreads[device.getId()] = producer

        numConsumers = int(len(self.devices) / self.PRODUCERS_PER_CONSUMER)
        # in the special case of only one device this will end up being zero so we manually set it to 1
        if len(self.devices) == 1:
            numConsumers = 1

        if numConsumers > 1:
            mismatch: bool = len(
                self.devices) % self.PRODUCERS_PER_CONSUMER != 0
            for i in range(numConsumers):
                startIdx = self.PRODUCERS_PER_CONSUMER * i
                numDevices = self.PRODUCERS_PER_CONSUMER
                if i == numConsumers - 1 and mismatch:
                    # in the case of devices left over, we append them to the last consumer if there are less than 50%
                    # of the expected producers per consumer. else, we add one last consumer to take care of the rest
                    leftOver = len(self.devices) - startIdx - 1
                    if leftOver < int(numConsumers / 2):
                        numDevices += leftOver
                    else:
                        self.consumerThreads.append(WorkerThread(name=f'Consumer-{startIdx + numDevices - 1}',
                                                                 target=self._consumeDataFromDevices, args=(self.errorQueue, startIdx + numDevices - 1, leftOver,)))

                self.consumerThreads.append(WorkerThread(name=f'Consumer-{startIdx}',
                                                         target=self._consumeDataFromDevices, args=(self.errorQueue, startIdx, numDevices,)))
        else:
            self.consumerThreads.append(WorkerThread(name=f'Consumer-0',
                                                     target=self._consumeDataFromDevices, args=(self.errorQueue, 0, 1,)))

        for device in self.devices:
            device.connect()

        self._inCollectionEpisode = True
        for producer in self.producerThreads.values():
            producer.start()
        for consumer in self.consumerThreads:
            consumer.start()
        self.outputThread.start()

        # begin the error-handling procedure on the main thread till we stop data collection
        self._handleErrorsInQueue()

    def stopDataCollection(self) -> None:
        if not self._inCollectionEpisode:
            raise NotInCollectionEpisodeError()
        for device in self.devices:
            device.stopDataCollection()

        self._inCollectionEpisode = False
        anyThreadsAlive: bool = True
        while anyThreadsAlive:
            anyThreadsAlive = False
            for producer in self.producerThreads.values():
                producer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= producer.isAlive()
            for consumer in self.consumerThreads:
                consumer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= consumer.isAlive()
            self.outputThread.join(self.THREAD_JOIN_TIMEOUT)
            anyThreadsAlive |= self.outputThread.isAlive()
        self.databaseWriter.disconnect()

        for device in self.devices:
            device.disconnect()

