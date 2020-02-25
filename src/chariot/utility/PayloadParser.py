from chariot.utility.exceptions import NoIdentifierError


class PayloadParser:
    # The purpose of this class is to parse payloads and check for certain criteria in the payloads. This allows
    # for parsing to be turned into function rather than be repeated in the api class.
    @staticmethod
    def getNameInPayload(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get('NetworkName')
        return networkName

    @staticmethod
    def getNameInURL(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.args['NetworkName']
        return networkName

    @staticmethod
    def getNetworkDescription(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get('Description')
        return networkName

    @staticmethod
    def getNewNetworkName(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        newNetworkName: str = requestContent.get('NewName')
        return newNetworkName

    @staticmethod
    def getDeviceNameInPayload(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get('DeviceName')
        if not deviceName:
            raise NoIdentifierError('device name')
        return deviceName

    @staticmethod
    def getDeviceNameInURL(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.args['DeviceName']
        if not deviceName:
            raise NoIdentifierError('device name')
        return deviceName
