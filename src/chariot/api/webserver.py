import flask
from typing import Dict
from flask import jsonify, request, session
from flask_cors import CORS
from chariot.device import DeviceAdapterFactory, DeviceConfigurationFactory
from chariot.device.adapter import DeviceAdapter
from chariot.configuration import Configuration
from chariot.database.configuration import DatabaseConfiguration
from chariot.database import DatabaseConfigurationFactory, DatabaseWriterFactory
from chariot.database.writer import DatabaseWriter
from chariot.utility import PayloadParser
from chariot.network import Network, NetworkManager
from chariot.utility.exceptions import NameNotFoundError, DuplicateNameError, ItemNotSupported, DatabaseConnectionError, \
    NoIdentifierError, ErrorStrings, LoginFailure, AuthenticationFailure
from chariot.network.configuration import NetworkConfiguration
from chariot.database import DatabaseManager
from chariot.utility.TypeStrings import TypeStrings
from flask_pymongo import PyMongo
from chariot.user import UserConfiguration, User
from functools import wraps

app = flask.Flask(__name__)
app.secret_key = "Chariot"  # Used to encrypt/decrypt data for session
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
CORS(app)  # This will enable CORS for all routes
app.config["DEBUG"] = True
mongo = PyMongo(app)

users = mongo.db.users  # table used to contain users profiles
nManagerBaseUrl: str = '/chariot/api/v1.0'
parser: PayloadParser = PayloadParser()
defaultSuccessCode: int = 200


def ensureLoggedIn(fn):
    # https: // www.rithmschool.com / courses / intermediate - flask / cookies - sessions - flask
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            raise AuthenticationFailure(ErrorStrings.ERR_Not_Authenticated.value, 401)
        return fn(*args, **kwargs)

    return wrapper


# --- This section deals with login and registration --- #
@app.route(nManagerBaseUrl + '/register', methods=['POST'])
def register():
    requestContent = request.get_json()
    userConfig: UserConfiguration = UserConfiguration(requestContent)
    username = userConfig.getId()

    # with the configuration set, check MongoDB to ensure username is unique
    existingUser = users.find_one({str(userConfig.getIdField()): username})

    if existingUser is None:
        # go ahead and store user in db
        users.insert_one(userConfig.toDict())
    else:
        # throw error indicating username is taken
        raise DuplicateNameError(
            ErrorStrings.ERR_Not_Unique_Name.value.format(userConfig.getId(), username)
        )

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/login', methods=['POST'])
def login():
    requestContent = request.get_json()
    username = requestContent.get("username")
    password = requestContent.get("password")

    # authenticate username/password
    loginUser = users.find_one({"username": username})

    if loginUser and loginUser["password"] == password:
        # authentication successful, create user object (removing _id to pass validation)
        config = loginUser
        del config["_id"]
        session["user"] = loginUser["username"]

        # fill the NetworkManager and DatabaseManager with configurations
        try:
            for networkMap in loginUser[TypeStrings.Network_Type.value]:
                listOfDevices = networkMap[TypeStrings.Device_Type.value]

                networkOnly = {}
                networkOnly[TypeStrings.Network_Identifier.value] = networkMap[TypeStrings.Network_Identifier.value]
                networkDescription = networkMap["description"]
                if networkDescription:
                    networkOnly["description"] = networkDescription
                else:
                    networkOnly["description"] = ""

                networkConfiguration: NetworkConfiguration = NetworkConfiguration(networkOnly)
                network: Network = Network(networkConfiguration)

                # add in devices to network
                for device in listOfDevices:
                    deviceMap = device
                    keysToDelete = []

                    # remove fields that have None/Null as value in order to pass validation
                    for item in deviceMap.items():
                        if not item[1]:
                            keysToDelete.append(item[0])

                    for key in keysToDelete:
                        del deviceMap[key]

                    # build configuration for device
                    deviceConfig: Configuration = DeviceConfigurationFactory.getInstance(deviceMap)

                    # with configuration validated, now use the factory to create a deviceAdapter instance
                    device: DeviceAdapter = DeviceAdapterFactory.getInstance(deviceConfig)

                    network.addDevice(device)
                NetworkManager.addNetwork(network)
        except KeyError:
            # no "network" array so there is no data to read
            pass

        # fill the NetworkManager and DatabaseManager with configurations
        try:
            for dbMap in loginUser[TypeStrings.Database_Type.value]:
                databaseMap = dbMap

                # remove fields that have None/Null as value in order to pass validation
                keysToDelete = []
                for item in databaseMap.items():
                    if not item[1]:
                        keysToDelete.append(item[0])

                for key in keysToDelete:
                    del databaseMap[key]

                dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(databaseMap)

                # with configuration validated, now use the factory to create a dbWriter instance
                dbWriter: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)

                # add to dbManager
                DatabaseManager.addDbWriter(dbWriter)
        except KeyError:
            pass  # no db configurations found for user


    else:
        raise LoginFailure(ErrorStrings.ERR_Login_Failed.value, 401)

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/logout', methods=['POST'])
def logout():
    session.pop("user", None)
    # Clean up NetworkManager and DatabaseManager
    NetworkManager.clearCollection()
    DatabaseManager.clearCollection()
    return buildSuccessfulRequest(None, defaultSuccessCode)


# --- This section of api endpoints deals with netowrks  --- #

@app.route(nManagerBaseUrl + '/networks/names', methods=['GET'])
@ensureLoggedIn  # must have user credentials in order to view results
# This method will return all network names known to the networkManager and their descriptions
def retrieveAllNetworkNames():
    allNetworks: Dict[str, str] = NetworkManager.getAllNetworks()
    return buildSuccessfulRequest(allNetworks, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/networks/all', methods=['GET'])
@ensureLoggedIn
# This method will return all known networks along with their devices
def retrieveAllNetworkDetails():
    networksAndDevices = NetworkManager.getNetworksAndDevices()
    return buildSuccessfulRequest(networksAndDevices, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['POST'])
@ensureLoggedIn
def createNetwork():
    requestContent = request.get_json()

    # build a NetworkConfiguration from payload and verify it
    networkConfig: NetworkConfiguration = NetworkConfiguration(requestContent)

    # if configuration is successful, then create a Network and add it to the NetworkManager
    network: Network = Network(networkConfig)
    NetworkManager.addNetwork(network)

    # update the user's networks in the db
    username: str = getCurrentUserName()

    # update the network key in db
    users.update_one({"username": username}, {'$push': {TypeStrings.Network_Type.value:
                                                            network.toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['PUT'])
@ensureLoggedIn
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
        requestContent[TypeStrings.Network_Identifier.value] = requestContent[parser.getNewNetworkNameStr()]
        del requestContent[parser.getNewNetworkNameStr()]

    # at this point, 'newNetworkName' is not a key, so validate configuration and update
    NetworkManager.getNetwork(networkName).updateConfig(requestContent)

    # if applicable, modify collection so the new network name is in collection and old one is deleted
    if hasNewName:
        newNetworkName: str = requestContent[TypeStrings.Network_Identifier.value]
        # notice that requestContent[TypeStrings.Network_Identifier.value] is used, this will return the new name since
        # keys were updated. So 'networkName' would be the old name of the network
        NetworkManager.replaceNetwork(networkName, newNetworkName)

        # update the database. Note how the newNetworkName is used
        users.update_one(
            {"username": getCurrentUserName(), "network.networkName": networkName},
            {'$set': {TypeStrings.Network_Type.value + ".$":
                          NetworkManager.getNetwork(newNetworkName).toDict()}})
    else:
        # no new network name is provided, simply update the values in db
        users.update_one(
            {"username": getCurrentUserName(), "network.networkName": networkName},
            {'$set': {TypeStrings.Network_Type.value + ".$":
                          NetworkManager.getNetwork(networkName).toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['DELETE'])
@ensureLoggedIn
def deleteNetwork():
    networkToDelete = parser.getNameInURL(request)
    NetworkManager.deleteNetwork(networkToDelete)

    # update the user's networks in the db
    username: str = getCurrentUserName()

    # update the network key in db
    users.update_one({"username": username},
                     {"$pull": {TypeStrings.Network_Type.value: {"networkName": networkToDelete}}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network', methods=['GET'])
@ensureLoggedIn
def getNetworkDetails():
    # this method returns an instantiated network's details
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
@ensureLoggedIn
def getDeviceDetails():
    # ensure that a network is specified in the payload
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.getNetwork(networkName)

    # find device in network
    deviceName: str = parser.getDeviceNameInURL(request)
    deviceConfig: Configuration = network.getDevice(deviceName).getConfiguration()

    return buildSuccessfulRequest(deviceConfig.toDict(), defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['POST'])
@ensureLoggedIn
def createDevice():
    # ensure that a network is specified in the payload
    requestContent = request.get_json()
    networkName = parser.getNameInPayload(requestContent)

    network: Network = NetworkManager.getNetwork(networkName)

    # build dictionary from payload and remove non-device fields
    payloadConfig = requestContent
    del payloadConfig[TypeStrings.Network_Identifier.value]

    # build configuration for device
    deviceConfig: Configuration = DeviceConfigurationFactory.getInstance(payloadConfig)

    # with configuration validated, now use the factory to create a deviceAdapter instance
    device: DeviceAdapter = DeviceAdapterFactory.getInstance(deviceConfig)

    # add device to specified network
    network.addDevice(device)

    # store this new device to database
    users.update_one({"username": getCurrentUserName(), "network.networkName": networkName},
                     {'$push': {TypeStrings.Network_Type.value + ".$." + TypeStrings.Device_Type.value:
                                    device.toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['PUT'])
@ensureLoggedIn
def modifyDevice():
    # through this endpoint, a device can have its configuration changed
    # it must be that the old name('deviceId') is specified and a new name('newDeviceId') is given in the payload
    requestContent = request.get_json()
    newDeviceName: str = None
    networkName = parser.getNameInPayload(requestContent)
    deviceName: str = parser.getDeviceNameInPayload(requestContent)

    # check if a new device name is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewDeviceIdStr() in requestContent:
        newDeviceName = requestContent[parser.getNewDeviceIdStr()]
        requestContent[TypeStrings.Device_Identifier.value] = newDeviceName
        del requestContent[parser.getNewDeviceIdStr()]

    # remove networkName and deviceType key so that updating configuration does not raise an error
    del requestContent[TypeStrings.Network_Identifier.value]
    del requestContent["deviceType"]

    NetworkManager.getNetwork(networkName).getDevice(deviceName).updateConfig(requestContent)

    # if applicable, modify collection so the new device name is in collection and old one is deleted
    if newDeviceName:
        NetworkManager.getNetwork(networkName).replaceDevice(deviceName, newDeviceName)
        users.update_one({"username": getCurrentUserName(), "network.networkName": networkName},
                         {'$set': {TypeStrings.Device_Type.value + ".$":
                                       NetworkManager.getNetwork(networkName).getDevice(newDeviceName).toDict()}})
    else:
        users.update_one({"username": getCurrentUserName(), "network.networkName": networkName},
                         {'$set': {TypeStrings.Device_Type.value + ".$":
                                       NetworkManager.getNetwork(networkName).getDevice(deviceName).toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/network/device', methods=['DELETE'])
@ensureLoggedIn
def deleteDevice():
    # ensure that a network is specified in the payload
    networkName = parser.getNameInURL(request)
    network: Network = NetworkManager.getNetwork(networkName)

    deviceName = parser.getDeviceNameInURL(request)

    # now delete device from specified network
    network.deleteDevice(deviceName)

    # delete from database
    users.update_one({"username": getCurrentUserName(), "network.networkName": networkName},
                     {'$pull': {TypeStrings.Network_Type.value + ".$." + TypeStrings.Device_Type.value:
                                    {TypeStrings.Device_Identifier.value: deviceName}}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


# ---  This section of endpoints deals with databases  --- #
@app.route(nManagerBaseUrl + '/database/test', methods=['POST'])
@ensureLoggedIn
def testDBConfiguration():
    # one can test an already created configuration or by payload
    requestContent = request.get_json()
    dbId = parser.getDbNameInPayload(requestContent)

    try:
        dbWriter: DatabaseWriter = DatabaseManager.getDbWriter(dbId)
        dbWriter.connect()
    except NameNotFoundError:
        # if the name isn't found in collection, do not throw error as this can be to test
        # a non-managed configuration
        pass
    except Exception as e:
        raise DatabaseConnectionError(str(e))

    # from the payload, create a dbWriter and test the connection
    dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(requestContent)
    # with configuration validated, now use the factory to create a dbWriter instance
    dbWriter: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)
    try:
        dbWriter.connect()
    except Exception as e:
        raise DatabaseConnectionError(str(e))

    dbWriter.disconnect()

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['POST'])
@ensureLoggedIn
def createDBConfiguration():
    payloadConfig = request.get_json()

    dbConfig: DatabaseConfiguration = DatabaseConfigurationFactory.getInstance(payloadConfig)

    # with configuration validated, now use the factory to create a dbWriter instance
    dbWriter: DatabaseWriter = DatabaseWriterFactory.getInstance(dbConfig)

    # add to dbManager
    DatabaseManager.addDbWriter(dbWriter)

    # update db
    users.update_one({"username": getCurrentUserName()},
                     {'$push': {TypeStrings.Database_Type.value: dbConfig.toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['PUT'])
@ensureLoggedIn
def modifyDatabaseConfiguration():
    # through this endpoint, a database can have its id and/or attributes changed
    # it must be that the old name('dbId') is specified and a new name('newDbId') is given in the payload
    requestContent = request.get_json()
    dbId: str = parser.getDbNameInPayload(requestContent)
    newDbId: str = None

    # check if a new dbId is specified in the payload, if so capture old name so its deleted from collection
    if parser.getNewDbIdStr() in requestContent:
        newDbId = requestContent[parser.getNewDbIdStr()]
        # for configuration validation, alter keys from 'dbId' to 'newDbId'
        requestContent[TypeStrings.Database_Identifier.value] = requestContent[parser.getNewDbIdStr()]
        del requestContent[parser.getNewDbIdStr()]

    # delete the type so validation passes
    del requestContent["type"]
    # at this point, 'newDbId' is not a key, so validate configuration and update
    DatabaseManager.getDbWriter(dbId).updateConfig(requestContent)

    # if applicable, modify collection so the new dbId is in collection and old one is deleted
    if newDbId:
        # notice that requestContent['dbId'] is used, this will return the new name since keys were
        # updated. So variable dbId would be the old name of the network
        DatabaseManager.replaceDbWriter(dbId, requestContent[TypeStrings.Database_Identifier.value])

        users.update_one({"username": getCurrentUserName(),
                          TypeStrings.Database_Type.value + "." + TypeStrings.Database_Identifier.value: dbId},
                         {'$set': {TypeStrings.Database_Type.value + ".$":
                          DatabaseManager.getDbWriter(newDbId).getConfiguration().toDict()}})
    else:
        users.update_one({"username": getCurrentUserName(),
                          TypeStrings.Database_Type.value + "." + TypeStrings.Database_Identifier.value: dbId},
                         {'$set': {TypeStrings.Database_Type.value + ".$":
                                       DatabaseManager.getDbWriter(dbId).getConfiguration().toDict()}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['DELETE'])
@ensureLoggedIn
def deleteDatabaseConfiguration():
    dbId = parser.getDbNameInURL(request)
    DatabaseManager.deleteDbWriter(dbId)

    users.update_one({"username": getCurrentUserName()},
                     {"$pull": {TypeStrings.Database_Type.value: {TypeStrings.Database_Identifier.value: dbId}}})

    return buildSuccessfulRequest(None, defaultSuccessCode)


@app.route(nManagerBaseUrl + '/database', methods=['GET'])
@ensureLoggedIn
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
@ensureLoggedIn
def retrieveAllDbConfigs():
    dbConfigs = DatabaseManager.getAllConfigurations()
    return buildSuccessfulRequest(dbConfigs, defaultSuccessCode)


# ---  This section deals with errorHandlers  --- #
@app.errorhandler(NameNotFoundError)
def handleNameNotFound(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


@app.errorhandler(NoIdentifierError)
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


@app.errorhandler(LoginFailure)
def handleLoginFailure(error):
    res = jsonify(toDict(error.message))
    res.status_code = error.status_code
    return res


@app.errorhandler(AuthenticationFailure)
def handleLoginFailure(error):
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


def getCurrentUserName():
    userName = session["user"]
    return userName


app.run()
