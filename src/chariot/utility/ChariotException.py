# Chariot Exceptions Library

class DeviceNotConnected(AssertionError):
    def __init__(self, deviceID: str):
        super().__init__(f'{deviceID} is not connected to the network.')

class InCollectionEpisodeError(AssertionError):
    def __init__(self,message):
        super().__init__('Network is in a Collection Episode.')

class NotInCollectionEpisodeError(AssertionError):
    def __init__(self):
        super().__init__('Network is not in a Collection Episode.')
