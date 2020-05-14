import pytest
import asyncio
import json
from typing import Awaitable, List, Optional
from chariot.collection.adapter import SocketServer

class SocketAdapterTest:
    instance: Optional[SocketServer] = None
    instance2: Optional[SocketServer] = None

    def createSocketServerTest(self):
        self.instance = SocketServer('localhost', 7654)
        assert self.instance is not None

    def socketStartTest(self):   
        self.instance = SocketServer('localhost', 7654)     
        self.instance.start()
        assert self.instance._running == True
        self.instance.stop()

    def socketStopTest(self):
        self.instance = SocketServer('localhost', 7655)
        self.instance.start()
        self.instance.stop()
        assert self.instance._running == False

    def createMultipleSocketsTest(self):
        self.instance = SocketServer('localhost', 7656)
        self.instance2 = SocketServer('localhost', 7657)
        
        self.instance.start()
        assert self.instance._running == True

        self.instance2.start()
        assert self.instance2._running == True

        self.instance.stop()
        assert self.instance._running == False

        self.instance2.stop()
        assert self.instance2._running == False

    def recycleSocketAddressTest(self):
        self.instance = SocketServer('localhost', 7658)
        self.instance.start()
        assert self.instance._running == True
        self.instance.stop()
        assert self.instance._running == False

        self.instance2 = SocketServer('localhost', 7658)
        with pytest.raises(OSError):
            self.instance2.start()
