from typing import List
from flask import Flask, request, app, jsonify, request
<<<<<<< HEAD

from chariot.core.network.Network import Network
from chariot.core.network.NetworkManager import NetworkManager

=======
from chariot.network import Network, NetworkManager
>>>>>>> master

nManagerBaseUrl: str = '/chariot/api/v1.0/networkManager'
networkManager = NetworkManager()


@app.route(nManagerBaseUrl + '/getAllNetworks', methods=['GET'])
<<<<<<< HEAD
# This method will return all networks known to the networkManager and
# their descriptions
def retrieveAllNetworkNames():
    # iterate over networkManager and create dict of networkName as key and
    # description as value
=======
# This method will return all networks known to the networkManager and their descriptions
def retrieveAllNetworkNames():
    # iterate over networkManager and create dict of networkName as key and description as value
>>>>>>> master
    allNames: List[str] = networkManager.getAllNetworkNames()
    return jsonify(allNames)


<<<<<<< HEAD
@app.route(
    nManagerBaseUrl +
    '/changeNetworkName/<str:netToModify>',
    methods=['POST'])
def modifyNetworkName(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(
            netToModify) is None:
=======
@app.route(nManagerBaseUrl + '/changeNetworkName/<str:netToModify>', methods=['POST'])
def modifyNetworkName(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(netToModify) is None:
>>>>>>> master
        # throw a 500 error
        pass

    requestContent = request.get_json()
    networkName: str = requestContent['Name']
    networkDesc: str = requestContent['Description']

    networkManager.modifyNetworkNameByName(networkName, netToModify)


<<<<<<< HEAD
@app.route(
    nManagerBaseUrl +
    '/changeNetworkDescription/<str:netToModify>',
    methods=['POST'])
def modifyNetworkDescription(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(
            netToModify) is None:
=======
@app.route(nManagerBaseUrl + '/changeNetworkDescription/<str:netToModify>', methods=['POST'])
def modifyNetworkDescription(netToModify):
    if netToModify is None or networkManager.findNetworkByNetworkName(netToModify) is None:
>>>>>>> master
        # throw a 500 error
        pass

    requestContent = request.get_json()
    networkDesc: str = requestContent['Description']

    networkManager.modifyNetworkDescriptionByName(networkDesc, netToModify)

<<<<<<< HEAD

@app.route(nManagerBaseUrl + '/delete/<str:netToDelete>', methods=['POST'])
def deleteNetwork(netToDelete):
    if netToDelete is None or networkManager.findNetworkByNetworkName(
            netToDelete) is None:
        # throw a 500 error
        pass

    networkManager.deleteNetworkByName(netToDelete)
=======
@app.route(nManagerBaseUrl + '/delete/<str:netToDelete>', methods=['POST'])
def deleteNetwork(netToDelete):
    if netToDelete is None or networkManager.findNetworkByNetworkName(netToDelete) is None:
        # throw a 500 error
        pass

    networkManager.deleteNetworkByName(netToDelete)
>>>>>>> master
