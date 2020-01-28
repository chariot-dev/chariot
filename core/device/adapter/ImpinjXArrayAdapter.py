from base64 import b64encode
from typing import Dict, Union
from core.JSONTypes import JSONObject
from core.device.adapter.DeviceAdapter import DeviceAdapter
from core.device.configuration.ImpinjXArrayConfiguration import ImpinjXArrayConfiguration

class ImpinjXArrayAdapter(DeviceAdapter):
    def __init__(self, config: ImpinjXArrayConfiguration):
        super().__init__(config)
        self.session: Union[Dict[str, str], None] = None

    def _buildSession(self):
        self.session = dict()
        self.session['connectUrl'] = self._getConnectUrl()
        

    def _getConnectUrl(self):
        return f'http://{self._config.ipAddress}/itemsense'
    
    def _generateBasicAuth(self, authStr: str):
        encoded = b64encode(authStr.encode())
        return f'Basic {encoded}'
    
    def captureData(self) -> JSONObject:
        if not self.connected:
            # raise DeviceNotConnected(?)Error
            raise AssertionError
        return None

    # any procedures necessary to start capturing data from the device
    def connect(self) -> None:
        self._buildSession()
        self.connected = True


    # gracefully close the connection to the device
    def disconnect(self) -> None:
        self.connected = False


__all__ = ['ImpinjXArrayAdapter']
