from .DeviceConfiguration import DeviceConfiguration

class DeviceAdapter:
    def __init__(self, _id: str, name: str, config: DeviceConfiguration):
        self.id = _id
        self.name = name
        self.unpackConfig(config)

     # get a packet of data from the device 
     def captureData():
        pass

    # gracefully close the connection to the device
    def cleanup():
        pass

    # any procedures necessary to start capturing data from the device
    def initialize():
        pass

    # all fields the class requires should be guaranteed to exist, so we set them without error checking
    # for optional fields, they are set as None if not set
    def unpackConfig(config: DeviceConfiguration):
        self.nickname = config.nickname
