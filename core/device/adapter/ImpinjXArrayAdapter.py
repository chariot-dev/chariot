from core.device.DeviceAdapter import DeviceAdapter
from core.device.configuration.ImpinjXArrayConfiguration import ImpinjXArrayConfiguration

class ImpinjXArrayAdapter(DeviceAdapter):
    def __init__(self, config: ImpinjXArrayConfiguration):
        super().__init__(config)

    def captureData(self) -> JSONObject:
        if not self.connected:
            # raise DeviceNotConnected(?)Error
            raise AssertionError
        return None

    # any procedures necessary to start capturing data from the device
    def connect(self) -> None:
        pass

    # gracefully close the connection to the device
    def disconnect(self) -> None:
        pass


__all__ = ['ImpinjXArrayAdapter']
