# Chariot Exceptions Library

class DeviceNotConnected(AssertionError):
    def __init__(self):
        super().__init__('Device is not connected to the network.')

class InCollectionEpisodeError(AssertionError):
    def __init__(self):
        super().__init__('Network is in a Collection Episode.')

class NotInCollectionEpisodeError(AssertionError):
    def __init__(self):
        super().__init__('Network is not in a Collection Episode.')
