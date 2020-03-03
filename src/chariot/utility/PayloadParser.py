from chariot.utility.exceptions import NoIdentifierError, ErrorStrings


class PayloadParser:
    # The purpose of this class is to parse payloads and check for certain criteria in the payloads. This allows
    # for parsing to be turned into function rather than be repeated in the api class.

    def __init__(self):
        self.networkNameStr: str = 'networkName'
        self.newNetworkNameStr: str = 'newNetworkName'
        self.descriptionStr: str = 'description'
        self.deviceIdStr: str = 'deviceId'
        self.newDeviceIdStr: str = 'newDeviceId'

    def getNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get(self.networkNameStr)
        return networkName

    def getNameInURL(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.args[self.networkNameStr]
        if networkName is None:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Network_Identifier.value
            )
        return networkName

    def getNetworkDescription(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get(self.descriptionStr)
        return networkName

    def getNewNetworkName(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        newNetworkName: str = requestContent.get(self.networkNameStr)
        return newNetworkName

    def getDeviceNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get(self.deviceIdStr)
        return deviceName

    def getNewDeviceNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get(self.newDeviceIdStr)
        return deviceName

    def getDeviceNameInURL(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.args[self.deviceIdStr]
        if not deviceName:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Device_Identifier.value
            )
        return deviceName
