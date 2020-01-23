from core.device.DeviceAdapter import DeviceAdapter
from core.device.configuration.ImpinjR420Configuration import ImpinjR420Configuration

class ImpinjR420Adapter(DeviceAdapter):
    def __init__(self, config: ImpinjR420Configuration):
        self.config: ImpinjR420Configuration = config
        self.connected: bool = False

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


__all__ = ['ImpinjR420Adapter']
