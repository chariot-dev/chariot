from collections import OrderedDict
from threading import Thread
# unused right now, but will be useful for scaling past a couple of devices
from multiprocessing.queues import Queue as ProcessQueue
from typing import List, OrderedDict, Tuple, Type, Union
from queue import Empty as QueueEmptyException, Queue as ThreadQueue
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.JSONTypes import JSONObject
from chariot.network.Network import Network
from chariot.network.NetworkManager import NetworkManager
from chariot.utility.ChariotExceptions import *

class ProducerThread(Thread):
    pass


class ConsumerThread(Thread):
    pass


class DataCollectionManager:
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network
    DEFAULT_TIMEOUT = 5
    ERROR_CHECK_TIMEOUT = 0.5
    PRODUCERS_PER_CONSUMER = 2

    # TODO: complete handleError method to continuously examine the error queue
    # TODO: when DatabaseWriter is implemented, remove quotes around type definition
    # TODO: add __del__ method to stop data collection when this object goes out of scope
    # TODO: add DataOutputStream for outputThread to also send data to
    def __init__(self, network: Union[Network, None], dbWriter: 'DatabaseWriter'):
        self.activeNetwork: Union[Network, None] = network
        self.devices: List[DeviceAdapter] = network.getDevices() if network is not None else []
        self.consumerThreads: List[ConsumerThread] = []
        self.producerThreads: OrderedDict[str, ProducerThread] = OrderedDict()
        self.outputThread: ConsumerThread = ConsumerThread(
            target=self._outputData)
        self.errorQueue: ThreadQueue = ThreadQueue()
        self.dataQueue: ThreadQueue = ThreadQueue()
        self.databaseWriter: 'DatabaseWriter' = dbWriter
        self._inCollectionEpisode: bool = False
        self._episodeStartTime: float = 0.0

    def _consumeDataFromDevice(self, deviceIdx: int) -> None:
        device: DeviceAdapter = self.devices[deviceIdx]
        while self._inCollectionEpisode:
            output: List[JSONObject] = []
            try:
                data: JSONObject = device.getDataQueue().get(block=True, timeout=DEFAULT_TIMEOUT)
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
                        data: JSONObject = self.devices[i].getDataQueue().get_nowait()
                        output.append(data)
                    except QueueEmptyException:
                        continue
                if len(output) > 0:
                    self.dataQueue.put(output, block=True)

    def _handleErrorsInQueue(self) -> None:
        disconnectedDevices: OrderedDict[str, int] = OrderedDict()          #Tracks how many attempts there were to reconnect

        while self._inCollectionEpisode:
            try:
                # Errors received are a tuple of the Thread name/id and the stacktrace 
                deviceID ,error = self.errorQueue.get(block=True, timeout=ERROR_CHECK_TIMEOUT)
                # handling error logic goes here - based on the type of the error we either continue
                # or stop the whole episode

                # For making changes to the correct device in the ProducerThreads List
                errorDevice: DeviceAdapter = self.activeNetwork.getDeviceByDeviceName(deviceID)
                exc_type, exc_val, exc_trace = error

                if isinstance(exc_val, DeviceNotConnectedError):

                    if deviceID in disconnectedDevices:
                        if disconnectedDevices[deviceID] > 3:
                            disconnectedDevices[deviceID] += 1
                        elif disconnectedDevices[deviceID] == 3:
                            #LOG: f'{deviceID} has failed to reconnect. Stopping collection from device.'
                            errorDevice.stopDataCollection()
                            disconnectedDevices[deviceID] += 1
                        else: 
                            #LOG: f'Attemtpting to reconnect to {deviceID}'
                            errorDevice.connect()
                            disconnectedDevices[deviceID] += 1
                    else:
                            disconnectedDevices[deviceID] = 1
                            errorDevice.connect()
                elif isinstance(exc_val, InCollectionEpisodeError):
                    #handle error
                    pass
                elif isinstance(exc_val, NotInCollectionEpisodeError):
                    #handle error
                    pass
                else:                              #Unkown error, crash system for now
                    self.stopDataCollection()
            except QueueEmptyException:
                continue

    # use get then get_nowait logic here as well
    def _outputData(self) -> None:
        while self._inCollectionEpisode:
            output: List[JSONObject] = []
            try:
                data: JSONObject = self.dataQueue.get(block=True, timeout=DEFAULT_TIMEOUT)
                output.append(data)
            except QueueEmptyException:
                pass

            while True:
                try:
                    data: JSONObject = self.dataQueue.get_nowait()
                    output.append(data)
                except QueueEmptyException:
                    break
            self.databaseWriter.insertMany(output)

    def inCollectionEpisode(self) -> bool:
        return self._inCollectionEpisode

    def setActiveNetwork(self, network: Union[Network, None]):
        if self._inCollectionEpisode:
            # can't set an active network during a data collection episode
            # to support concurrent network data collection, a new instance of DataCollectionManager has to be spawned
            raise InCollectionEpisodeError()
        self.activeNetwork = network
        self.devices = network.getDevices()

    def getActiveNetwork(self) -> Network:
        return self.activeNetwork

    def beginDataCollection(self) -> None:
        if self._inCollectionEpisode:
            raise InCollectionEpisodeError()

        if len(self.devices) == 0:
            # can't collect data from a network with no devices
            raise AssertionError('Must have at least one device to collect from.')
        for device in self.devices:
            producer = ProducerThread(
                name=f'Producer_{device.getId()}', target=device.beginDataCollection, args=(self.errorQueue,))
            self.producerThreads[device.getId()] = producer

        numConsumers = int(len(devices) / PRODUCERS_PER_CONSUMER)
        # in the special case of only one device this will end up being zero so we manually set it to 1
        if len(devices) == 1:
            numConsumers = 1

        if numConsumers > 1:
            mismatch: bool = len(devices) % PRODUCERS_PER_CONSUMER != 0
            for i in range(numConsumers):
                startIdx = PRODUCERS_PER_CONSUMER * i
                numDevices = PRODUCERS_PER_CONSUMER
                if i == numConsumers - 1 and mismatch:
                    # in the case of devices left over, we append them to the last consumer if there are less than 50%
                    # of the expected producers per consumer. else, we add one last consumer to take care of the rest
                    leftOver = len(devices) - startIdx - 1
                    if leftOver < int(numConsumers / 2):
                        numDevices += leftOver
                    else:
                        self.consumerThreads.append(ConsumerThread(
                            target=self._consumeDataFromDevices, args=(startIdx + numDevices - 1, leftOver,)))

                # TODO: add names of devices assigned as names of the threads for easier debugging
                self.consumerThreads.append(ConsumerThread(
                    target=self._consumeDataFromDevices, args=(startIdx, numDevices,)))
        else:
            self.consumerThreads.append(ConsumerThread(
                target=self._consumeDataFromDevices, args=(0, 1,)))

        self._inCollectionEpisode = True

        for producer in self.producerThreads:
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
        for producer in self.producerThreads:
            producer.join()
        for consumer in self.consumerThreads:
            consumer.join()
        self.outputThread.join()
