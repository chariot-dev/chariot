from sys import exc_info
from traceback import format_exception
from multiprocessing import Process


class HandledProcess(Process):
    def run(self):
        try:
            if self._target:
                self._target(*self._args[1:], **self._kwargs)
        except Exception as err:
            # add the error to the errorQueue for handling on the main thread
            # args[0]: the errorQueue passed in
            print(err)
            self._args[0].put((self.name, err, format_exception(*exc_info())))
