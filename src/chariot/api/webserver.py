import flask
from typing import Dict
from flask import jsonify, request
from flask_cors import CORS
from chariot.device import DeviceAdapterFactory, DeviceConfigurationFactory
from chariot.device.adapter import DeviceAdapter
from chariot.configuration import Configuration
from chariot.database.configuration import DatabaseConfiguration
from chariot.database import DatabaseConfigurationFactory, DatabaseWriterFactory
from chariot.database.writer import DatabaseWriter
from chariot.utility import PayloadParser
from chariot.network import Network, NetworkManager
from chariot.utility.exceptions import NameNotFoundError, DuplicateNameError, ItemNotSupported, DatabaseConnectionError
from chariot.network.configuration import NetworkConfiguration
from chariot.database import DatabaseManager
from chariot.utility import TypeStrings

app = flask.Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.config["DEBUG"] = True

nManagerBaseUrl: str = '/chariot/api/v1.0'
parser: PayloadParser = PayloadParser()
defaultSuccessCode: int = 200


# --- This section of api endpoints deals with netowrks  --- #

@app.route(nManagerBaseUrl + '/networks/names', methods=['GET'])
# This method will return all network names known to the networkManager and their descriptions
def retrieveAllNetworkNames():
    allNetworks: Dict[str, str] = NetworkManager.getAllNetworks()
    return buildSuccessfulRequest(allNetworks, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/networks/all', methods=['GET'])
# This method will return all known networks along with their devices
def retrieveAllNetworkDetails():
    networksAndDevices = NetworkManager.getNetworksAndDevices()
    return buildSuccessfulRequest(networksAndDevices, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['POST'])
def createNetwork():
    requestContent = request.get_json()

    # build a NetworkConfiguration from payload and verify it
    networkConfig: NetworkConfiguration = NetworkConfiguration(requestContent)

    # if configuration is successful, then create a Network and add it to the NetworkManager
    network: Network = Network(networkConfig)
    NetworkManager.addNetwork(network)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['PUT'])
def modifyNetwork():
    # through this endpoint, a network can have its name and/or description changed
    # it must be that the old name('networkName') is specified and a new name('newNetworkName') is given in the payload

    requestContent = request.get_json()
    hasNewName = False
    networkName: str = parser.getNameInPayload(requestContent)

    # check if a new network name is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewNetworkNameStr() in requestContent:
        hasNewName = True
        # for configuration validation, alter keys from 'newNetworkName' to 'networkName'
        requestContent[TypeStrings.Network_Identifier] = requestContent[parser.getNewNetworkNameStr()]
        del requestContent[parser.getNewNetworkNameStr()]

    # at this point, 'newNetworkName' is not a key, so validate configuration and update
    NetworkManager.getNetwork(networkName).getConfiguration().updateConfig(requestContent)

    # if applicable, modify collection so the new network name is in collection and old one is deleted
    if hasNewName:
        # notice that requestContent[TypeStrings.Network_Identifier] is used, this will return the new name since
        # keys were updated. So 'networkName' would be the old name of the network
        NetworkManager.replaceNetwork(requestContent[TypeStrings.Network_Identifier], networkName)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['DELETE'])
def deleteNetwork():
    networkToDelete = parser.getNameInURL(request)
    NetworkManager.deleteNetwork(networkToDelete)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['GET'])
def getNetworkDetails():
    # this method returns a specific network details
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.getNetwork(networkName).getConfiguration().toDict()

    return buildSuccessfulRequest(network, defaultSuccessCode)


# ---  This section of endpoints deals with devices  --- #

@app.route(nManagerBaseUrl + '/network/device/supportedDevices', methods=['GET'])
def getSupportedDevices():
    # returns a dictionary of supported devices, with key as deviceType and value as the configuration
    return buildSuccessfulRequest(DeviceAdapterFactory.getsupportedDevices(), None)


@app.route(nManagerBaseUrl + '/network/device/config', methods=['GET'])
def getSupportedDeviceConfig():
    deviceTemplateName = parser.getDeviceNameInURL(request)

    # get specified device template
    deviceTemplate = DeviceAdapterFactory.getSpecifiedDeviceTemplate(deviceTemplateName)

    return buildSuccessfulRequest(deviceTemplate, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['GET'])
def getDeviceDetails():
    # ensure that a network is specified in the payload
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.getNetwork(networkName)

    # find device in network
    deviceName: str = parser.getDeviceNameInURL(request)
    deviceConfig: Configuration = network.getDevice(deviceName).getConfiguration()

    return buildSuccessfulRequest(deviceConfig.toDict(), defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['POST'])
def createDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = parser.getNameInPayload(requestContent)

    network: Network = NetworkManager.getNetwork(networkName)

    # build dictionary from payload and remove non-device fields
    payloadConfig = requestContent
    del payloadConfig[TypeStrings.Network_Identifier]

    # build configuration for device
    deviceConfig: Configuration = DeviceConfigurationFactory.getInstance(payloadConfig)

    # with configuration validated, now use the factory to create a deviceAdapter instance
    device: DeviceAdapter = DeviceAdapterFactory.getInstance(deviceConfig)

    # add device to specified network
    network.addDevice(device)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['PUT'])
def modifyDevice():
    # through this endpoint, a device can have its configuration changed
    # it must be that the old name('deviceId') is specified and a new name('newDeviceId') is given in the payload
    requestContent = request.get_json()
    hasNewName = False
    networkName = parser.getNameInPayload(requestContent)
    deviceName: str = parser.getDeviceNameInPayload(requestContent)

    # check if a new device name is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewDeviceIdStr() in requestContent:
        hasNewName = True
        requestContent[TypeStrings.Device_Identifier] = requestContent[parser.getNewDeviceIdStr()]
        del requestContent[parser.getNewDeviceIdStr()]

    NetworkManager.getNetwork(networkName).getDevice(deviceName).getConfiguration().updateConfig(requestContent)

    # if applicable, modify collection so the new device name is in collection and old one is deleted
    if hasNewName:
        NetworkManager.getNetwork(networkName).replaceDevice(requestContent[TypeStrings.Device_Identifier], deviceName)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['DELETE'])
def deleteDevice():
    # ensure that a network is specified in the payload
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.getNetwork(networkName)

    deviceName = parser.getDeviceNameInURL(request)

    # now delete device from specified network
    network.deleteDevice(deviceName)
    return buildSuccessfulRequest(None, defaultSuccessCode)


# ---  This section of endpoints deals with databases  --- #
@app.route(nManagerBaseUrl + '/database/test', methods=['POST'])
def testDBConfiguration():
    payloadConfig = request.get_json()

    dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(payloadConfig)

    # with configuration validated, now use the factory to create a dbWriter instance
    dbWriter: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)

    try:
        dbWriter.connect()
    except Exception as e:
        raise DatabaseConnectionError(str(e))

    dbWriter.disconnect()

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['POST'])
def createDBConfiguration():
    payloadConfig = request.get_json()

    dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(payloadConfig)

    # with configuration validated, now use the factory to create a dbWriter instance
    dbWriter: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)

    # add to dbManager
    DatabaseManager.addDbWriter(dbWriter)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['PUT'])
def modifyDatabaseConfiguration():
    # through this endpoint, a database can have its id and/or attributes changed
    # it must be that the old name('dbId') is specified and a new name('newDbId') is given in the payload

    requestContent = request.get_json()
    hasNewName = False
    dbId: str = parser.getDbNameInPayload(requestContent)

    # check if a new dbId is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewDbIdStr() in requestContent:
        hasNewName = True
        # for configuration validation, alter keys from 'dbId' to 'newDbId'
        requestContent[TypeStrings.Database_Identifier] = requestContent[parser.getNewDbIdStr()]
        del requestContent[parser.getNewDbIdStr()]

    # at this point, 'newDbId' is not a key, so validate configuration and update
    DatabaseManager.getDbWriter(dbId).getConfiguration().updateConfig(requestContent)

    # if applicable, modify collection so the new dbId is in collection and old one is deleted
    if hasNewName:
        # notice that requestContent['dbId'] is used, this will return the new name since keys were
        # updated. So variable dbId would be the old name of the network
        DatabaseManager.replaceDbWriter(requestContent[TypeStrings.Database_Identifier], dbId)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['DELETE'])
def deleteDatabaseConfiguration():
    dbId = parser.getNameInURL(request)
    DatabaseManager.deleteDbWriter(dbId)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['GET'])
def getDatabaseConfiguration():
    # this method returns a specific database config
    dbId = parser.getDbNameInURL(request)
    db: DatabaseWriter = DatabaseManager.getDbWriter(dbId).getConfiguration().toDict()

    return buildSuccessfulRequest(db, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database/supportedDatabases', methods=['GET'])
def getSupportedDatabases():
    # returns a dictionary of supported devices, with key as deviceType and value as the configuration
    return buildSuccessfulRequest(DatabaseWriterFactory.getsupportedDatabases(), None)


@app.route(nManagerBaseUrl + '/database/config', methods=['GET'])
def getSupportedDatabaseConfig():
    deviceTemplateName = parser.getDbNameInURL(request)

    # get specified device template
    deviceTemplate = DatabaseWriterFactory.getSpecifiedDbTemplate(deviceTemplateName)

    return buildSuccessfulRequest(deviceTemplate, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database/all', methods=['GET'])
# This method will return all known networks along with their devices
def retrieveAllDbConfigs():
    dbConfigs = DatabaseManager.getAllConfigurations()
    return buildSuccessfulRequest(dbConfigs, defaultSuccessCode)


# ---  This section deals with errorHandlers  --- #
@app.errorhandler(NameNotFoundError)
def handleInvalidUsage(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


@app.errorhandler(DuplicateNameError)
def handleDuplicateName(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


@app.errorhandler(ItemNotSupported)
def handleItemNotSupported(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


@app.errorhandler(DatabaseConnectionError)
def handleDatabaseNotConnected(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


# -- useful utility methods --
def toDict(e):
    rv = dict()
    rv["message"] = e
    return rv


def buildSuccessfulRequest(data, code):
    # NOTE: data should be in dictionary format
    if data is None:
        data = {'success': True}

    if code is None:
        code = 200

    response = jsonify(data)

    return response, code


app.run()
