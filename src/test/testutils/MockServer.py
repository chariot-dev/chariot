from flask import Flask, request
from flask_cors import CORS
from multiprocessing import Process
import random
import string
from chariot.utility.JSONTypes import JSONObject

class MockServer:
    RANDOM_STR_LEN = 100

    def __init__(self, port: int = 6000):
        self._port = port
        self._app: Flask = self._buildApp()
        self._appProcess = Process(name='Mock-Server-Process', target=self.run,
            kwargs={'debug': True, 'port': self._port, 'use_reloader': False, 'threaded': True})
        self._running = False

    def _buildApp(self) -> Flask:
        # Flask server in a package: https://flask.palletsprojects.com/en/1.1.x/api/
        app = self._buildEndpoints(Flask(__name__.split('.')[0]))
        CORS(app)
        return app

    def _buildEndpoints(self, app: Flask) -> Flask:
        app.add_url_rule('/data', None, self._getMockData)
        return app

    def _getMockData(self) -> JSONObject:
        strLen: int = request.args.get('strLen')
        if not strLen:
            strLen = self.RANDOM_STR_LEN
        return {'data': random.randint(0, strLen)}

    def isRunning(self) -> bool:
        return self._running

    def run(self, **kwargs) -> None:
        self._app.run(**kwargs)

    def start(self) -> None:
        self._appProcess.start()
        self._running = True

    def stop(self) -> None:
        if self._appProcess.is_alive():
            self._appProcess.terminate()
            self._appProcess.join()
            self._running = False
