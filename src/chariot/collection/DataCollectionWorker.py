from math import ceil
from multiprocessing import Event
from time import sleep
from typing import Callable, Dict, List, Optional, Set
from queue import SimpleQueue as Queue, Empty as QueueEmptyException
from chariot.device.adapter import DeviceAdapter
from chariot.utility.concurrency import HandledThread
from chariot.utility.exceptions.ChariotExceptions import *
from chariot.utility.JSONTypes import JSONObject


class DataCollectionWorker:
    DEFAULT_TIMEOUT: float = 1.0
    ERROR_CHECK_TIMEOUT: float = 0.5
    OUTPUT_WRITE_SLEEP: float = 2.0
    PRODUCERS_PER_CONSUMER: int = 2
    THREAD_JOIN_TIMEOUT: float = 1.0

    def __init__(self, devices: List[DeviceAdapter], minPollDelay: float = 0.01):
        self._devices = devices
        self._dataQueue: Queue = Queue()
        self._errorQueue: Queue = Queue()
        self._consumerThreads: List[HandledThread] = []
        self._minPollDelay: float = minPollDelay
        self._outputDelay: float = max(self._minPollDelay, self.OUTPUT_WRITE_SLEEP)
        self._running: bool = False
        self._producerThreads: Dict[str, HandledThread] = {}
        self._outputHooks: Set[Callable] = set()
        self._outputThread: Optional[HandledThread] = None
        self._stopThread: Optional[HandledThread] = None

    def __del__(self) -> None:
        self.stop()

    def _consumeDataFromDevice(self, deviceIdx: int) -> None:
        device: DeviceAdapter = self._devices[deviceIdx]
        while self._running:
            sleep(self._minPollDelay)
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
            if len(output) > 0:
                self._dataQueue.put(output, block=True)

    def _consumeDataFromDevices(self, startIdx: int, numDevices: int) -> None:
        if numDevices == 1:
            self._consumeDataFromDevice(startIdx)
        else:
            endIdx: int =  min(startIdx + numDevices, len(self._devices))
            while self._running:
                sleep(self._minPollDelay / numDevices)
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

    def _outputData(self) -> None:
        numDevices: int = len(self._devices)
        pollDelay = self._minPollDelay / numDevices
        while self._running:
            sleep(self._outputDelay)
            output: List[List[JSONObject]] = []
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
                self._callOutputHooks(chunk)

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

    def start(self, stopEvent: Event) -> None:
        if self._running:
            raise AssertionError

        if len(self._devices) == 0:
            raise AssertionError('Must have at least one device to collect from.')

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
            for i in range(0, totalDevices, avgProducersPerConsumer):
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
        for consumer in self._consumerThreads:
            consumer.start()
        for producer in self._producerThreads.values():
            producer.start()
        self._outputThread = HandledThread(name='Output-Handler', target=self._outputData, args=(self._errorQueue,))
        self._outputThread.start()
        self._stopThread = HandledThread(name='Stop-Sentinel', target=self._waitForStopEvent, args=(self._errorQueue, stopEvent,))
        self._stopThread.start()

    def _waitForStopEvent(self, event: Event) -> None:
        event.wait()
        self.stop()

    def stop(self, *args) -> None:
        if not self._running:
            return
        for device in self._devices:
            device.stopDataCollection()

        self._running = False
        anyThreadsAlive: bool = True
        while anyThreadsAlive:
            anyThreadsAlive = False
            for producer in self._producerThreads.values():
                producer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= producer.is_alive()
            for consumer in self._consumerThreads:
                consumer.join(self.THREAD_JOIN_TIMEOUT)
                anyThreadsAlive |= consumer.is_alive()
            self._outputThread.join(self.THREAD_JOIN_TIMEOUT)
            anyThreadsAlive |= self._outputThread.is_alive()
        self._consumerThreads.clear()
        self._producerThreads.clear()
