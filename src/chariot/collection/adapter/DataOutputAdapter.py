from abc import ABC
from multiprocessing import SimpleQueue as Queue
from typing import List
from chariot.utility.JSONTypes import JSONObject


class DataOutputAdapter(ABC):
    def __init__(self):
        self._dataQueue: Queue = Queue()

    def enqueue(self, record: JSONObject) -> None:
        self._dataQueue.put((record,))

    def enqueueMany(self, records: List[JSONObject]) -> None:
        self._dataQueue.put(records)
