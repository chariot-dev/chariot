import json
import flask
from typing import List, Dict
from flask import jsonify, request, app
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
    allNetworks: Dict[str, str] = NetworkManager.getAllNetworkNamesAndDesc()
    return buildSuccessfulRequest(allNetworks, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/networks/all', methods=['GET'])
# This method will return all known networks along with their devices
def retrieveAllNetworkDetails():
    networksAndDevices = NetworkManager.getAllNetworkNamesAndDevices()
    return buildSuccessfulRequest(networksAndDevices, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['POST'])
def createNetwork():
    requestContent = request.get_json()

    # check that a network name is specified in the payload
    networkName = parser.getNameInPayload(requestContent)
    networkDesc: str = parser.getNetworkDescription(requestContent)  # note that description is optional

    NetworkManager.addNetwork(networkName, networkDesc)
    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['PUT'])
def modifyNetwork():
    # through this endpoint, a network can have its name and/or description changed
    # it must be that the old name('networkName') is specified and a new name('NewName') is given in the payload
    requestContent = request.get_json()
    hasNewName = True

    # check that a network name is specified in the payload
    oldNetworkName = parser.getNameInPayload(requestContent)
    # check that a new name is found in the payload
    newName = parser.getNewNetworkName(requestContent)

    networkDesc: str = parser.getNetworkDescription(requestContent)  # note that description is optional

    if newName is not None:
        NetworkManager.modifyNetworkNameByName(newName, oldNetworkName)
    else:
        # no NewName for network provided
        hasNewName = False

    if networkDesc is not None:
        if hasNewName:
            NetworkManager.modifyNetworkDescriptionByName(networkDesc, newName)
        else:
            NetworkManager.modifyNetworkDescriptionByName(networkDesc, oldNetworkName)
    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['DELETE'])
def deleteNetwork():
    networkToDelete = parser.getNameInURL(request)
    NetworkManager.deleteNetworkByName(networkToDelete)
    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['GET'])
def getNetworkDetails():
    # this method returns a specific network details
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # convert into JSON and return
    return buildSuccessfulRequest(network.toString(), defaultSuccessCode)


# ---  This section of endpoints deals with devices  --- #

@app.route(nManagerBaseUrl + '/network/devices/supportedDevices', methods=['GET'])
def getSupportedDevices():
    return buildSuccessfulRequest(DeviceAdapterFactory.getsupportedDevices())


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
    # it must be that the old name('deviceId') is specified and a new name('NewDeviceId') is given in the payload

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

    return buildSuccessfulRequest(None, defaultSuccessCode)


# ---  This section deals with errorHandlers  --- #
@app.errorhandler(NameNotFoundError)
def handleInvalidUsage(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


@app.errorhandler(DuplicateNameError)
def handleDuplicateName(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


@app.errorhandler(DeviceNotSupported)
def handleDeviceNotSupported(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


@app.errorhandler(DatabaseConnectionError)
def handleDatabaseNotConnected(error):
    res = jsonify(error.to_dict())
    res.status_code = error.status_code
    return res


# -- useful utility methods --
def to_dict(e):
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
