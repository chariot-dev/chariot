from flask import Flask, request
# from flask_cors import CORS
from multiprocessing import Process
import random
import string
from chariot.utility.JSONTypes import JSONObject

class MockServer:
    RANDOM_STR_LEN = 10

    def __init__(self, port: int = 6000):
        self.port = port
        self.app: Flask = self._buildApp()
        self.appProcess = Process(name='Mock-Server-Process', target=self.run,
            kwargs={'debug': True, 'port': self.port, 'use_reloader': False, 'threaded': True})

    def _buildApp(self) -> Flask:
        # Flask server in a package: https://flask.palletsprojects.com/en/1.1.x/api/
        app = self._buildEndpoints(Flask(__name__.split('.')[0]))
        return app

    def _buildEndpoints(self, app: Flask) -> Flask:
        app.add_url_rule('/data', None, self._getMockData)
        return app

    def _getMockData(self) -> JSONObject:
        strLen: int = request.args.get('strLen')
        if not strLen:
            strLen = self.RANDOM_STR_LEN
        # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
        return {
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=strLen)),
            'info': ''.join(random.choices(string.ascii_uppercase + string.digits, k=strLen)),
        }

    def run(self, **kwargs) -> None:
        self.app.run(**kwargs)

    def start(self) -> None:
        self.appProcess.start()

    def stop(self) -> None:
        self.appProcess.terminate()
        self.appProcess.join()
