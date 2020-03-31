from sys import exc_info
from time import time
from traceback import print_tb
from threading import Thread

class HandledThread(Thread):
    def run(self):
        try:
            if self._target:
                self._target(*self._args[1:], **self._kwargs)
        except Exception as err:
            # add the error to the errorQueue for handling on the main thread
            # args[0]: the errorQueue passed in
            trace = exc_info()
            print_tb(trace[2])
            print(f'{err} at {time()}')
            self._args[0].put((self.name, exc_info()))
        finally:
            # https://github.com/python/cpython/blob/9c87fbe54e1c797e3c690c6426bdf5e79c457cf1/Lib/threading.py#L872
            del self._target, self._args, self._kwargs
