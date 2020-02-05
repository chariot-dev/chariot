from chariot.device import DeviceAdapter


class Network:
    networkBaseUrl: str = '/chariot/api/v1.0/network'

    def __init__(self, networkName: str, networkDesc: str):
        self.networkName = networkName
        self.networkDesc = networkDesc
        self.devices: DeviceAdapter = []

    def modifyNetworkName(self, newName: str):
        self.networkName = newName

    def modifyNetworkDesc(self, newDesc: str):
        self.networkDesc = newDesc

    def getNetworkName(self) -> str:
        return self.networkName

    def getNetworkDesc(self) -> str:
        return self.networkDesc

    # figure out how much error-checking to do
    def addDevice(self, device: DeviceAdapter):
        # Currently just restricting adding a device that already exists in collection
        if self.getDeviceByDeviceName(device.getDeviceName()) is None:
            self.devices.append(device)
        # else: have a device by the same name already in collection

    def getDeviceByDeviceName(self, nameToFind: str) -> DeviceAdapter:
        i: int = 0
        while i < len(self.devices):
            if self.devices[i].getDeviceName == nameToFind:
                return self.devices[i]

    def getDeviceIndexByName(self, nameToFind: str) -> int:
        i: int = 0
        while i < len(self.devices):
            if self.devices[i].getDeviceName == nameToFind:
                return i
            i = i + 1
        return -1

    def getDeviceByIndex(self, index: int) -> DeviceAdapter:
        if index - 1 > len(self.devices) or index < 0:
            print("Invalid index given for device lookup.")
        return self.devices[index]

    def deleteDeviceByName(self, deviceName: str):
        deviceIndex: int = self.getDeviceIndexByName(deviceName)
        if deviceIndex == -1:
            print(" Device {} not found in Network ", deviceName)
        else:
            del self.devices[deviceIndex]

    def deleteDeviceByIndex(self, index: int):
        if index - 1 > len(self.devices) or index < 0:
            print(" Invalid index given for deletion of device")
        else:
            del self.devices[index]

    # importDeviceConfig
    # exportNetwork - again seems like a utility method
    # saveNetwork - idea is to save this network configuration to the UserAccount
    # modifyDevice - need to figure out how to be able to do this for each device, given that each one
    # has different variables
