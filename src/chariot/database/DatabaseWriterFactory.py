from typing import Dict, Type
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.database.writer.MongoDatabaseWriter import MongoDatabaseWriter
from chariot.database.writer.MySQLDatabaseWriter import MySQLDatabaseWriter
from chariot.database.configuration.DatabaseConfiguration import DatabaseConfiguration
from chariot.utility.AbstractFactory import AbstractFactory
from os import path
from chariot.utility.JSONTypes import JSONDict
from json import load
from chariot.utility.exceptions.ErrorStrings import ErrorStrings
from chariot.utility.exceptions.CustomExceptions import ItemNotSupported



class _DatabaseWriterFactory(AbstractFactory):
    def __init__(self):
        self.instanceMap: Dict[str, Type[DatabaseWriter]] = {
            'MongoDB': MongoDatabaseWriter,
            'MySQL': MySQLDatabaseWriter
        }
        self.instanceName: str = 'database'
        self.typeField: str = 'type'

        currentPath = path.dirname(path.abspath(__file__))
        try:
            with open(f'{currentPath}/templates/GenericRequiredFields.json') as genericTemplate:
                self._genericRequiredTemplate = load(genericTemplate)
        except IOError:
            raise ItemNotSupported(
                ErrorStrings.ERR_Generic_Device_Template.value.format("/templates/GenericRequiredFields.json")
            )
    
    def getInstance(self, config: DatabaseConfiguration) -> DatabaseWriter:
        return super().getInstance(config)
    
    def getsupportedDatabases(self) -> JSONDict:
        # update each device configuration with generic required fields
        fullDb: Dict[str, DatabaseConfiguration] = {}

        for db in self.instanceMap.keys():
            fullDb.update(self.getSpecifiedDbTemplate(db))
        return fullDb
    
    def getDbInformation(self, dbName: str) -> JSONDict:
        if dbName not in self.instanceMap.keys():
            raise ItemNotSupported(ErrorStrings.ERR_Item_Not_Supported.value.format(self.instanceName, dbName))
        return self._supportedDevices[dbName]

    # this method returns a specified device json file
    def getSpecifiedDbTemplate(self, dbName) -> JSONDict:
        # build path to json file
        currentPath = path.dirname(path.abspath(__file__))
        try:
            with open(f'{currentPath}/templates/{dbName}.json') as dbTemplate:
                # now combine the specified device template with that of the generic template
                specificDb = load(dbTemplate)
                return self.combineConfigWithGeneric(specificDb, dbName)
        except:
            raise ItemNotSupported(ErrorStrings.ERR_Item_Not_Supported.value.format(self.instanceName, dbName))

    # use this method to combine settings from a specific configuration instance with the generic required fields
    def combineConfigWithGeneric(self, config: JSONDict, dbType: str):
        combinedDict = config

        # combine settings of the config with the generic required fields
        for field in self._genericRequiredTemplate["settings"]:
            combinedDict[dbType]["settings"].insert(0, field)  # add required field add beginning of list

        return combinedDict


# Return singleton
DatabaseWriterFactory = _DatabaseWriterFactory()

__all__ = ['DatabaseWriterFactory']
