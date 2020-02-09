import json
import flask
from typing import List, Dict
from flask import jsonify, request
from flask_cors import CORS

from chariot.device.DeviceAdapterFactory import DeviceAdapterFactory
from chariot.device.adapter.DeviceAdapter import DeviceAdapter
from chariot.device.configuration import DeviceConfiguration
from chariot.device.configuration import ImpinjR420Configuration
from chariot.device.configuration import ImpinjXArrayConfiguration
from chariot.utility.PayloadParser import PayloadParser
from chariot.network import Network
from chariot.network import NetworkManager

app = flask.Flask(__name__)
CORS(app) # This will enable CORS for all routes
app.config["DEBUG"] = True

nManagerBaseUrl: str = '/chariot/api/v1.0/'

# --- This section of api endpoints deals with netowrks  --- #

@app.route(nManagerBaseUrl + '/networks/names', methods=['GET'])
# This method will return all network names known to the networkManager and their descriptions
def retrieveAllNetworkNames():
    allNetworks: Dict[str, str] = NetworkManager.getAllNetworkNames()
    return jsonify(allNetworks)


@app.route(nManagerBaseUrl + '/networks/all', methods=['GET'])
# This method will return all known networks along with their devices
def retrieveAllNetworkDetails():
    pass


@app.route(nManagerBaseUrl + '/network/', methods=['POST'])
def createNetwork():
    requestContent = request.get_json()

    # check that a network name is specified in the payload
    networkName = PayloadParser.checkForNetworkName(requestContent)

    networkDesc: str = requestContent.get('Description', defaultValue='')  # note that description is optional

    NetworkManager.addNetwork(networkName, networkDesc)


@app.route(nManagerBaseUrl + '/network/', methods=['POST'])
def modifyNetwork():
    # through this endpoint, a network can have its name and/or description changed
    # it must be that the old name('Name') is specified and a new name('NewName') is given in the payload
    requestContent = request.get_json()

    # check that a network name is specified in the payload
    oldNetworkName = PayloadParser.checkForNetworkName(requestContent)
    # check that a new name is found in the payload
    newName = PayloadParser.checkForNewNetworkName(requestContent)

    networkDesc: str = requestContent.get('Description', defaultValue='')  # note that description is optional

    NetworkManager.modifyNetworkNameByName(newName, oldNetworkName)
    if networkDesc:
        NetworkManager.modifyNetworkDescriptionByName(networkDesc, newName)


@app.route(nManagerBaseUrl + '/network/', methods=['DELETE'])
def deleteNetwork():
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    NetworkManager.deleteNetworkByName(networkName)


@app.route(nManagerBaseUrl + '/network/', methods=['GET'])
def getNetworkDetails():
    # this method returns a specific network details
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # convert into JSON and return
    return json.dumps(network)


# ---  This section of endpoints deals with devices  --- #

@app.route(nManagerBaseUrl + 'network/devices/supportedDevices', methods=['GET'])
def getSupportedDevices():
    return jsonify(DeviceAdapterFactory.getsupportedDevices())

@app.route(nManagerBaseUrl + 'network/device/config', methods=['GET'])
def getSupportedDeviceConfig():
    deviceTemplateName = request.args['DeviceName']
    deviceTemplate = DeviceAdapterFactory.getSpecifiedDeviceTemplate(deviceTemplateName)
    
    return jsonify(deviceTemplate)

    #requestContent = request.get_json()
    #deviceTemplateName = requestContent['DeviceName']
    #get specified device template
    #deviceTemplate = DeviceAdapterFactory.getSpecifiedDeviceTemplate(deviceTemplateName)
    #return jsonify(deviceTemplate)


@app.route(nManagerBaseUrl + 'network/device', methods=['GET'])
def getDeviceDetails():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    # find device in network
    device = network.getDeviceByDeviceName(requestContent['deviceName'])

    return jsonify(device)


@app.route(nManagerBaseUrl + 'network/device', methods=['POST'])
def createDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    deviceToCreate: str = ''
    configurationInstance: DeviceConfiguration
    supportedDevices = DeviceAdapterFactory.getsupportedDevices()

    # need to find which of the supported devices is found in the payload
    if requestContent['deviceToCreate'] in supportedDevices:
        deviceToCreate: str = requestContent['deviceToCreate']

    # now that specific device has been identified, ensure that configuration variables are filled correctly
    if deviceToCreate == "Impinj xArray":
        configurationInstance = ImpinjXArrayConfiguration(requestContent[deviceToCreate])
    elif deviceToCreate == "Impinj Speedway R420":
        configurationInstance = ImpinjR420Configuration(requestContent[deviceToCreate])
    else:
        # device user wants to create is not supported raise error
        pass

    # now use the factory to create a deviceAdapter instance
    device: DeviceAdapter = DeviceAdapterFactory(configurationInstance)

    # add device to specified network
    network.addDevice(device)


@app.route(nManagerBaseUrl + 'network/device', methods=['PUT'])
def modifyDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

@app.route(nManagerBaseUrl + 'network/device', methods=['DELETE'])
def deleteDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = PayloadParser.checkForNetworkName(requestContent)
    network: Network = NetworkManager.findNetworkByNetworkName(networkName)

    deviceName = PayloadParser.checkForDeviceName(requestContent)

    #now delete device from specified network
    network.deleteDeviceByName(deviceName)

app.run()