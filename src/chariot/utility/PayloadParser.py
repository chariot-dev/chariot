from chariot.utility.exceptions import NoIdentifierError
from chariot.utility.exceptions.ErrorStrings import ErrorStrings


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
        if networkName is None:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Network_Identifier.value
            )
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
        deviceName: str = requestContent.get('deviceId')
        return deviceName

    @staticmethod
    def getNewDeviceNameInPayload(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get('NewDeviceId')
        return deviceName

    @staticmethod
    def getDeviceNameInURL(requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.args['deviceId']
        if not deviceName:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Device_Identifier.value
            )
        return deviceName
