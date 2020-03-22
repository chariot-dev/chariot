from math import ceil
from time import time
from threading import Thread
from typing import Callable, Dict, List, Set
from queue import SimpleQueue as Queue, Empty as QueueEmptyException
from chariot.device.adapter import DeviceAdapter
from chariot.utility.concurrency import HandledThread
from chariot.utility.exceptions.ChariotExceptions import *
from chariot.utility.JSONTypes import JSONObject


class DataCollectionWorker:
    DEFAULT_TIMEOUT: float = 5.0
    ERROR_CHECK_TIMEOUT: float = 0.5
    PRODUCERS_PER_CONSUMER: int = 2
    THREAD_JOIN_TIMEOUT: float = 2.0

    def __init__(self, devices: List[DeviceAdapter]):
        self._devices = devices
        self._dataQueue: Queue = Queue()
        self._errorQueue: Queue = Queue()
        self._consumerThreads: List[HandledThread] = []
        self._running: bool = False
        self._producerThreads: Dict[str, HandledThread] = {}
        self._outputHooks: Set[Callable] = set()
        self._outputThread: HandledThread(name='Output-Handler', target=self._outputData, args=(self._errorQueue,))

    def _consumeDataFromDevice(self, deviceIdx: int) -> None:
        device: DeviceAdapter = self._devices[deviceIdx]
        device.connect()
        while self._running:
            output: List[JSONObject] = []
            try:
                data: JSONObject = device.getDataQueue().get(
                    block=True, timeout=self.DEFAULT_TIMEOUT)
                output.append(data)
            except QueueEmptyException:
                pass

            while True:
                try:
                    data: JSONObject = device.getDataQueue().get(block=False)
                    output.append(data)
                except QueueEmptyException:
                    break
            self._dataQueue.put(output, block=True)
        device.disconnect()

    def _consumeDataFromDevices(self, startIdx: int, numDevices: int) -> None:
        if numDevices == 1:
            self._consumeDataFromDevice(startIdx)
        else:
            endIdx: int =  min(startIdx + numDevices, len(self._devices))
            for i in range(startIdx, endIdx):
                self._devices[i].connect()
            while self._running:
                output: List[JSONObject] = []
                for i in range(startIdx, endIdx):
                    try:
                        data: JSONObject = self._devices[i].getDataQueue(
                        ).get(block=False)
                        output.append(data)
                    except QueueEmptyException:
                        continue
                if len(output) > 0:
                    self._dataQueue.put(output, block=True)

        for i in range(startIdx, endIdx):
            self._devices[i].disconnect()

    def _outputData(self) -> None:
        while self._running:
            output: List[JSONObject] = []
            try:
                data: List[JSONObject] = self._dataQueue.get(
                    block=True, timeout=self.DEFAULT_TIMEOUT)
                output.append(data)
            except QueueEmptyException:
                pass

            while True:
                try:
                    data = self._dataQueue.get(block=False)
                    output.append(data)
                except QueueEmptyException:
                    break
            for chunk in output:
                self._callOutputHooks(data)

    def addOutputHook(self, hook: Callable) -> None:
        self._outputHooks.add(hook)

    def _callOutputHooks(self, data: JSONObject) -> None:
        for hook in self._outputHooks:
            hook(data)

    def clearOutputHooks(self) -> None:
        self._outputHooks.clear()

    def getErrorQueue(self) -> Queue:
        return self._errorQueue

    def isRunning(self) -> bool:
        return self._running

    def removeOutputHook(self, hook: Callable) -> None:
        self._outputHooks.remove(hook)

    def start(self) -> None:
        if self._running:
            raise AssertionError

        if len(self._devices) == 0:
            raise AssertionError(
                'Must have at least one device to collect from.')
        for device in self._devices:
            producer = HandledThread(
                name=f'Producer: {device.getId()}', target=device.startDataCollection, args=(self._errorQueue,))
            self._producerThreads[device.getId()] = producer

        totalDevices: int = len(self._devices)
        numConsumers: int = ceil(totalDevices / self.PRODUCERS_PER_CONSUMER)
        avgProducersPerConsumer: int = int(round(totalDevices / numConsumers))

        if totalDevices == 1:
            numConsumers = 1

        # split producers as equally as possible among consumers
        if numConsumers > 1:
            for i in range(0, numConsumers, avgProducersPerConsumer):
                startIdx: int = i
                # index error past the end of the array is handled in self._consumeDataFromDevices
                numDevices: int = avgProducersPerConsumer 
                consumer: HandledThread = HandledThread(name=f'Consumer-{startIdx}',
                    target=self._consumeDataFromDevices, args=(self._errorQueue, startIdx, numDevices,))
                self._consumerThreads.append(consumer)
        else:
            self._consumerThreads.append(HandledThread(name=f'Consumer-0',
                target=self._consumeDataFromDevices, args=(self._errorQueue, 0, 1,)))
        self._running = True
        for producer in self._producerThreads.values():
            producer.start()
        for consumer in self._consumerThreads:
            consumer.start()
        self._outputThread.start()

    def stop(self) -> None:
        if not self._running:
            return
        for device in self.devices:
            device.stopDataCollection()

        self._running = False
        anyThreadsAlive: bool = True
        while anyThreadsAlive:
            anyThreadsAlive = False
            for producer in self._producerThreads.values():
                producer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= producer.isAlive()
            for consumer in self._consumerThreads:
                consumer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= consumer.isAlive()
            self.outputThread.join(self.THREAD_JOIN_TIMEOUT)
            anyThreadsAlive |= self._outputThread.isAlive()
        self._consumerThreads.clear()
        self._producerThreads.clear()
