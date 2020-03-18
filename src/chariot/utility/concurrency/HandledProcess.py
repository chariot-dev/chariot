from sys import exc_info
from multiprocessing import Process

class HandledProcess(Process):
    def run(self):
        try:
            if self._target:
                self._target(*self._args[1:], **self._kwargs)
        except Exception as err:
            # add the error to the errorQueue for handling on the main thread
            # args[0]: the errorQueue passed in
           self._args[0].put((self.name, exc_info()))

