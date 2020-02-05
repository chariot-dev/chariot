from collections import OrderedDict
from threading import Thread
# unused right now, but will be useful for scaling past a couple of devices
from multiprocessing.queues import Queue as ProcessQueue
from typing import List, OrderedDict, Union
from queue import Empty as QueueEmptyException, Queue as ThreadQueue
from core.device.adapter.DeviceAdapter import DeviceAdapter
from core.JSONTypes import JSONObject
from core.network.Network import Network
from core.network.NetworkManager import NetworkManager


class ProducerThread(Thread):
    pass


class ConsumerThread(Thread):
    pass


class DataCollectionManager:
    # This class is intended to work with an instance of NetworkManager. The NetworkManager
    # is responsible for housing multiple user-defined networks. Once a network has been selected
    # for data collection, this class interacts with the NetworkManager to start and stop data collection
    # of all devices from the selected network
    PRODUCERS_PER_CONSUMER = 2

    # TODO: handleError method to continuously examine the error queue
    # TODO: when DatabaseWriter is implemented, remove quotes around type definition
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
            data: JSONObject = device.getDataQueue().get(block=True)
            output.append(data)

            while True:
                try:
                    data: JSONObject = device.getDataQueue().get(block=True)
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

    def _outputData(self) -> None:
        while self._inCollectionEpisode:
            data: List[JSONObject] = self.dataQueue.get(block=True)
            self.databaseWriter.insertRows(data)

    def inCollectionEpisode(self) -> bool:
        return self._inCollectionEpisode

    def setActiveNetwork(self, network: Union[Network, None]):
        if self._inCollectionEpisode:
            # can't set an active network during a data collection episode
            # to support concurrent network data collection, a new instance of DataCollectionManager has to be spawned
            raise AssertionError
        self.activeNetwork = network
        self.devices = network.getDevices()

    def getActiveNetwork(self) -> Network:
        return self.activeNetwork

    def beginDataCollection(self) -> None:
        if self._inCollectionEpisode:
            raise AssertionError

        if len(self.devices) == 0:
            # can't collect data from a network with no devices
            raise AssertionError
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

        for producer in self.producerThreads:
            producer.start()
        for consumer in self.consumerThreads:
            consumer.start()
        self.outputThread.start()

        # TODO: begin event-based loop to handle entries to errorQueue
        self._inCollectionEpisode = True

    def stopDataCollection(self) -> None:
        if not self._inCollectionEpisode:
            raise AssertionError
        for device in self.devices:
            device.stopDataCollection()
        for _, producer in self.producerThreads:
            producer.join()
        for consumer in self.consumerThreads:
            consumer.join()
        self.outputThread.join()
        self._inCollectionEpisode = False

    # This method is to handle ctrl-c in a graceful manner.
    # NOTE: Python signal handlers are always executed in the main Python thread
    # def handler(signum, frame):
        # Handle cleanup which is gracefully terminating data collection
        #print("SIGINT detected. Closing application.")
        # self.terminateDataCollection()


# Set the signal handler
#signal.signal(signal.CTRL_C_EVENT, handler)
