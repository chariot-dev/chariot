from typing import Dict
from chariot.database.writer.DatabaseWriter import DatabaseWriter
from chariot.utility import Manager


class _DatabaseManager(Manager):

    def __init__(self):
        # TODO: load all database configs for a user upon instantiation
        self.collection: Dict[str, DatabaseWriter] = {}

    def addDbWriter(self, dbWriter: DatabaseWriter) -> None:
        self._addToCollection(dbWriter)

    def deleteDbWriter(self, dbId: str) -> None:
        self._deleteFromCollection(dbId)

    def getDbWriter(self, dbId: str) -> DatabaseWriter:
        return self._retrieveFromCollection(dbId)

    # This method gives a new id to an already defined dbWriter in the collection and deletes the old one
    def replaceDbWriter(self, newName: str, toFind: str):
        self._modifyNameInCollection(newName, toFind)

    def getAllConfigurations(self) -> Dict[str, DatabaseWriter]:
        allConfigs: Dict[str, DatabaseWriter] = {}
        for key in self.collection:
            allConfigs[key] = self._retrieveFromCollection(key).getConfiguration().toDict()

        return allConfigs



# return a singleton instance
DatabaseManager = _DatabaseManager()

__all__ = ['DatabaseManager']
