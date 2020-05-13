from enum import Enum


class TypeStrings(Enum):
    Device_Type = 'device'
    Device_Identifier = 'deviceId'
    Network_Type = 'network'
    Network_Identifier = 'networkName'
    Database_Type = 'database'
    Database_Identifier = 'dbId'
    DataCollection_Identifier = 'configId'
