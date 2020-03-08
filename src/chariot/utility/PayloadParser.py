from chariot.utility.exceptions import ErrorStrings, NoIdentifierError
from chariot.utility.TypeStrings import TypeStrings


class PayloadParser:
    # The purpose of this class is to parse payloads and check for certain criteria in the payloads. This allows
    # for parsing to be turned into function rather than be repeated in the api class.

    def __init__(self):
        self.newNetworkNameStr: str = 'newNetworkName'
        self.descriptionStr: str = 'description'
        self.newDeviceIdStr: str = 'newDeviceId'
        self.newDbIdStr: str = 'newDbId'

    def getNewNetworkNameStr(self) -> str:
        return self.newNetworkNameStr

    def getDescriptionStr(self) -> str:
        return self.descriptionStr

    def getNewDeviceIdStr(self) -> str:
        return self.newDeviceIdStr

    def getNewDbIdStr(self) -> str:
        return self.newDbIdStr

    def getNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get(TypeStrings.Network_Identifier.value)
        return networkName

    def getNameInURL(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.args[TypeStrings.Network_Identifier.value]
        if networkName is None:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Identifier.value.format(TypeStrings.Network_Identifier.value)
            )
        return networkName

    def getNetworkDescription(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        networkName: str = requestContent.get(self.descriptionStr)
        return networkName

    def getNewNetworkName(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        newNetworkName: str = requestContent.get(TypeStrings.Network_Identifier.value)
        return newNetworkName

    def getDeviceNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get(TypeStrings.Device_Identifier.value)
        return deviceName

    def getNewDeviceNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.get(self.newDeviceIdStr)
        return deviceName

    def getDeviceNameInURL(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        deviceName: str = requestContent.args[TypeStrings.Device_Identifier.value]
        if not deviceName:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Identifier.value.format(TypeStrings.Device_Identifier.value)
            )
        return deviceName

    def getDbNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        dbId: str = requestContent.get(TypeStrings.Database_Identifier.value)
        return dbId

    def getNewDbNameInPayload(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        dbId: str = requestContent.get(self.newDbIdStr)
        return dbId

    def getDbNameInURL(self, requestContent) -> str:
        # first ensure that a network name has been given to specify which network is to be modified
        dbId: str = requestContent.args[TypeStrings.Database_Identifier.value]
        if not dbId:
            raise NoIdentifierError(
                ErrorStrings.ERR_Specify_Identifier.value.format(TypeStrings.Database_Identifier.value)
            )
        return dbId
