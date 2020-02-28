import requests
import json
from queue import Queue 
from base64 import b64encode
from json import dumps
from time import sleep
from typing import Dict, Union
from chariot.utility.JSONTypes import JSONDict, JSONObject
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration.ImpinjXArrayConfiguration import ImpinjXArrayConfiguration


class ItemsenseSession:
    def __init__(self):
        self.basicAuth: str = str()
        self.basicAuthHeaders: Dict[str, str] = {}
        self.dataRequestBody: Dict[str, str] = str()
        self.dataRequestUrl: str = str()
        self.connectUrl: str = str()
        self.jobId: str = str()
        self.token: str = str()
        self.tokenAuth: str = str()
        self.tokenAuthHeaders: Dict[str, str] = {}


# TODO: error checking all requests responses (try/catch blocks)
class ImpinjXArrayAdapter(DeviceAdapter):
    def __init__(self, config: ImpinjXArrayConfiguration):
        super().__init__(config)
        self.session: Union['ItemsenseSession', None] = None

    def _buildJobInfo(self) -> Dict[str, JSONObject]:
        jobInfo: Dict[str, str] = {}
        if(self._config.jobName):
            jobInfo['jobName'] = self._config.jobName
        if(self._config.facility):
            jobInfo['facility'] = self._config.facility
        if(self._config.startDelay):
            jobInfo['startDelay'] = self._config.startDelay
        if(self._config.readerGroups):
            jobInfo['readerGroups'] = self._config.readerGroups
        if(self._config.reportToDatabaseEnabled):
            jobInfo['reportToDatabaseEnabled'] = self._config.reportToDatabaseEnabled
        if(self._config.reportToHistoryEnabled):
            jobInfo['reportToHistoryEnabled'] = self._config.reportToHistoryEnabled
        if(self._config.reportToMessageQueueEnabled):
            jobInfo['reportToMessageQueueEnabled'] = self._config.reportToMessageQueueEnabled
        if(self._config.useOtherJobData):
            jobInfo['useOtherJobData'] = self._config.useOtherJobData
        return jobInfo

    def _buildSession(self):
        self.session = ItemsenseSession()
        self.session.connectUrl = self._getConnectUrl()
        self.session.dataRequestUrl = f'{self.session.connectUrl}/data/v1/items/show'
        self.session.basicAuth = self._generateBasicAuth(
            f'{self._config.authUsername}:{self._config.authPassword}')
        self.session.basicAuthHeaders = {
            'Authorization': self.session.basicAuth,
            'Content-Type': 'application/json'
        }
        self.session.token = self._getToken(
            self.session.connectUrl, self._config.authUsername)
        self.session.tokenAuth = 'Token {"token":"%s"}' % self.session.token
        self.session.tokenAuthHeaders = {
            'Authorization': self.session.tokenAuth,
            'Content-Type': 'application/json'
        }
        self.session.jobId = self._getItemsenseJobId(
            self.session.connectUrl, self.session.tokenAuth)
        self.session.dataRequestBody = {'jobId': self.session.jobId}
        if self._config.facility:
            self.session.dataRequestBody['facility'] = self._config.facility

    def _generateBasicAuth(self, authStr: str) -> str:
        encoded: bytes = b64encode(authStr.encode())
        return f'Basic {encoded.decode()}'

    def _getConnectUrl(self) -> str:
        return f'http://{self._config.ipAddress}/itemsense'

    def _getToken(self, connectUrl: str, authUsername: str) -> str:
        tokenUrl: str = f'{connectUrl}/authentication/v1/token/{authUsername}'
        response: requests.Response = requests.put(tokenUrl, { 'Authorization': tokenUrl })
        token: str = response.json()['token']
        return token

    def _getItemsenseJobId(self, connectUrl: str, tokenAuth: str) -> str:
        jobUrl: str = f'{connectUrl}/control/v1/jobs/start'
        jobInfo: Dict[str, JSONObject] = self._buildJobInfo()
        response: requests.Response = requests.post(
            jobUrl, data=dumps(jobInfo), headers=self.session.tokenAuthHeaders)
        jobId: str = response.json()['id']
        return jobId

    def _revokeAuthToken(self) -> None:
        revokeUrl = f'{self.session.connectUrl}/authentication/v1/revokeToken'
        tokenData: Dict[str, str] = {'token': self.sesion.token}
        response: requests.Response = requests.put(
            revokeUrl,
            data=json.dumps(tokenData),
            headers=self.session.basicAuthHeaders
            )
        return

    def _stopItemsenseJob(self) -> None:
        stopUrl = f'{self.session.connectUrl}/control/v1/jobs/stop/{self.session.jobId}'
        response: requests.Response = requests.post(stopUrl, headers=self.session.tokenAuthHeaders)
        return

    def beginDataCollection(self, errorQueue: Queue) -> None:
        self.inCollectionEpisode = True
        while self.inCollectionEpisode:
            if not self.connected:
                # raise DeviceNotConnected(?)Error
                stackTrace = self._generateStackTrace(AssertionError('Device was not connected'))
                errorQueue.put(stackTrace, block=True)
                self.stopDataCollection()
                # or continue? makes no difference
                break

            collectedAllPages: bool = False
            while not collectedAllPages:
                try:
                    response: requests.Response = requests.get(
                        self.session.dataRequestUrl,
                        data = dumps(self.session.dataRequestBody),
                        headers = self.session.tokenAuthHeaders
                        )
                    jsonData: JSONDict = response.json()
                    self.dataQueue.put(jsonData, block=True)
                    if 'nextPageMarker' in jsonData:
                        self.session.dataRequestBody['pageMarker'] = jsonData['nextPageMarker']
                    else:
                        collectedAllPages = True
                except Exception as err:
                    stackTrace = self._generateStackTrace(err)
                    errorQueue.put(stackTrace, block=True)
                sleep(self._config.pollDelay)
        self.session.dataRequestBody.pop('nextPageMarker', None)

    # any procedures necessary to start capturing data from the device
    def connect(self) -> None:
        self._buildSession()
        self.connected = True

    # gracefully close the connection to the device
    def disconnect(self) -> None:
        if not self.connected:
            # raise DeviceNotConnected(?)Error
            raise AssertionError
        self._stopItemsenseJob()
        self._revokeAuthToken()
        self.session = None
        self.connected = False


__all__=['ImpinjXArrayAdapter']
