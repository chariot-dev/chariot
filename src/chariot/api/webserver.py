import flask
from typing import Dict
from flask import jsonify, request
from flask_cors import CORS

from chariot.device.DeviceAdapterFactory import DeviceAdapterFactory
from chariot.device.DeviceConfigurationFactory import DeviceConfigurationFactory
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.configuration.Configuration import Configuration
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.database.DatabaseConfigurationFactory import DatabaseConfigurationFactory
from chariot.database.DatabaseWriterFactory import DatabaseWriterFactory
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.utility.PayloadParser import PayloadParser
from chariot.network.Network import Network
from chariot.network.NetworkManager import NetworkManager
from chariot.utility.exceptions.CustomExceptions import NameNotFoundError, DuplicateNameError, DeviceNotSupported
from chariot.utility.exceptions.CustomExceptions import DatabaseConnectionError
from chariot.network.configuration.NetworkConfiguration import NetworkConfiguration
from chariot.database.DatabaseManager import DatabaseManager

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
    networksAndDevices = NetworkManager.getDeviceNames()
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
        requestContent[parser.getNetworkNameStr()] = requestContent[parser.getNewNetworkNameStr()]
        del requestContent[parser.getNewNetworkNameStr()]

    # at this point, 'newNetworkName' is not a key, so validate configuration and update
    NetworkManager.getNetwork(networkName).getConfiguration.updateConfig(requestContent)

    # if applicable, modify collection so the new network name is in collection and old one is deleted
    if hasNewName:
        # notice that requestContent[parser.getNetworkNameStr()] is used, this will return the new name since keys were
        # updated. So 'networkName' would be the old name of the network
        NetworkManager.replaceNetwork(requestContent[parser.getNetworkNameStr()], networkName)

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
    network: Network = NetworkManager.replaceNetwork(networkName)

    return buildSuccessfulRequest(network.toDict(), defaultSuccessCode)


# ---  This section of endpoints deals with devices  --- #

@app.route(nManagerBaseUrl + '/network/devices/supportedDevices', methods=['GET'])
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
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # find device in network
    deviceName: str = parser.getDeviceNameInURL(request)
    deviceConfig: Configuration = network.getDeviceByDeviceName(deviceName).getDeviceConfiguration()

    return buildSuccessfulRequest(deviceConfig.toDict(), defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['POST'])
def createDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = parser.getNameInPayload(requestContent)

    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # build dictionary from payload and remove non-device fields
    payloadConfig = requestContent
    del payloadConfig["networkName"]

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

    # ensure that a network is specified in the payload
    requestContent = request.get_json()

    networkName = parser.getNameInPayload(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # now attempt to find device in the network
    deviceToFind: str = parser.getDeviceNameInPayload(requestContent)
    device: DeviceAdapter = network.getDeviceByDeviceName(deviceToFind)
    newName: str = parser.getNewDeviceNameInPayload(requestContent)

    oldConfiguration: Configuration = device.getDeviceConfiguration()

    # remove fields not in device configuration
    newConfiguration = requestContent
    del newConfiguration['networkName']

    if newName is not None:
        del newConfiguration['newDeviceId']

    # now attempt to modify device configuration
    oldConfiguration.modifyConfig(newConfiguration)

    # change name if user has requested so
    if newName is not None:
        network.modifyDeviceNameByName(newName, deviceToFind)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['DELETE'])
def deleteDevice():
    # ensure that a network is specified in the payload
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    deviceName = parser.getDeviceNameInURL(request)

    # now delete device from specified network
    network.deleteDeviceByName(deviceName)
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

    try:
        dbWriter.connect()
    except Exception as e:
        raise DatabaseConnectionError(str(e))

    dbWriter.disconnect()

    # add to dbManager
    DatabaseManager.addDbWriter(dbWriter)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['PUT'])
def modifyDatabaseConfiguration():
    # through this endpoint, a database can have its id and/or attributes changed
    # it must be that the old name('dbId') is specified and a new name('newDbId') is given in the payload

    requestContent = request.get_json()
    hasNewName = False
    dbId: str = parser.getDbInPayload(requestContent)

    # check if a new dbId is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewDbNameStr() in requestContent:
        hasNewName = True
        # for configuration validation, alter keys from 'dbId' to 'newDbId'
        requestContent['dbId'] = requestContent['newDbId']
        del requestContent['newDbId']

    # at this point, 'newDbId' is not a key, so validate configuration and update
    DatabaseManager.getDbWriter(dbId).modifyConfiguration(requestContent)

    # if applicable, modify collection so the new dbId is in collection and old one is deleted
    if hasNewName:
        # notice that requestContentrequestContent['dbId'] is used, this will return the new name since keys were
        # updated. So variable dbId would be the old name of the network
        DatabaseManager.replaceDbWriter(requestContent['dbId'], dbId)

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
    db: DatabaseWriter = DatabaseManager.getDbWriter(dbId)

    return buildSuccessfulRequest(DatabaseWriter.getConfiguration(), defaultSuccessCode)


# ---  This section of endpoints deals with devices  --- #

@app.route(nManagerBaseUrl + '/database/supportedDatabases', methods=['GET'])
def getSupportedDatabases():
    # returns a dictionary of supported devices, with key as deviceType and value as the configuration
    return buildSuccessfulRequest(DatabaseConfigurationFactory.getSupportedDatabases(), None)


@app.route(nManagerBaseUrl + '/database/config', methods=['GET'])
def getSupportedDatabaseConfig():
    deviceTemplateName = parser.getDeviceNameInURL(request)

    # get specified device template
    deviceTemplate = DeviceAdapterFactory.getSpecifiedDeviceTemplate(deviceTemplateName)

    return buildSuccessfulRequest(deviceTemplate, defaultSuccessCode)


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


@app.errorhandler(DeviceNotSupported)
def handleDeviceNotSupported(error):
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
