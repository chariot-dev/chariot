from core.device.configuration.DeviceConfiguration import DeviceConfiguration

class ImpinjXArrayConfiguration(DeviceConfiguration):
    def __init__(self, configMap):
        super().__init__(configMap)

    def _validateConfig(self, config) -> None:
        super()._validateConfig()

__all__ = ['ImpinjXArrayConfiguration']
