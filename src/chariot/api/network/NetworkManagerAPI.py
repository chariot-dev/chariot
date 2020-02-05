from typing import List
from flask import Flask, request, app, jsonify, request
from chariot.network import Network, NetworkManager

nManagerBaseUrl: str = '/chariot/api/v1.0/networkManager'
networkManager = NetworkManager()


@app.route(nManagerBaseUrl + '/getAllNetworks', methods=['GET'])
# This method will return all networks known to the networkManager and their descriptions
def retrieveAllNetworkNames():
    # iterate over networkManager and create dict of networkName as key and description as value
    allNames: List[str] = networkManager.getAllNetworkNames()
    return jsonify(allNames)


@app.route(nManagerBaseUrl + '/changeNetworkName/<str:netToModify>', methods=['POST'])
def modifyNetworkName(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(netToModify) is None:
        # throw a 500 error
        pass

    requestContent = request.get_json()
    networkName: str = requestContent['Name']
    networkDesc: str = requestContent['Description']

    networkManager.modifyNetworkNameByName(networkName, netToModify)


@app.route(nManagerBaseUrl + '/changeNetworkDescription/<str:netToModify>', methods=['POST'])
def modifyNetworkDescription(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(netToModify) is None:
        # throw a 500 error
        pass

    requestContent = request.get_json()
    networkDesc: str = requestContent['Description']

    networkManager.modifyNetworkDescriptionByName(networkDesc, netToModify)

@app.route(nManagerBaseUrl + '/delete/<str:netToDelete>', methods=['POST'])
def deleteNetwork(netToDelete):
    if netToDelete is None or networkManager.findNetworkByNetworkName(netToDelete) is None:
        # throw a 500 error
        pass

    networkManager.deleteNetworkByName(netToDelete)