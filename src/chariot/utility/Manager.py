from abc import ABC
from typing import Any, Dict, TypeVar
from chariot.utility.exceptions import NoIdentifierError, DuplicateNameError, NameNotFoundError, ErrorStrings

T = TypeVar('T')  # Declare type variable


class Manager(ABC):
    # this class will act as a base class for all manager classes. It will allow for management of items in a collection
    def __init__(self):
        self.collection: Dict[str, Any] = {}

    def _addToCollection(self, item: T) -> None:
        itemId: str = item.getConfiguration().getId()
        idField: str = item.getConfiguration().getIdField()
        if itemId is None:
            raise NoIdentifierError(ErrorStrings.ERR_Specify_Identifier.value.format(idField))

        # When adding a key, if the same key is in the dict, the values are overridden. Avoid this.
        if itemId not in self.collection:
            self.collection[itemId] = item
        else:
            raise DuplicateNameError(ErrorStrings.ERR_Not_Unique_Name.value.format(itemId, idField))

    def _deleteFromCollection(self, itemId: str):
        if itemId is None:
            raise NoIdentifierError(ErrorStrings.ERR_Specify_Identifier.value.format(ErrorStrings.Err_General_Id))

        if itemId in self.collection:
            del self.collection[itemId]
        else:
            raise NameNotFoundError(ErrorStrings.Err_Id_Not_In_Collection.value.format(itemId))

    # Convenience method used to return a generic object via a given network name
    def _retrieveFromCollection(self, itemId: str) -> T:
        try:
            item: T = self.collection[itemId]
        except KeyError:
            raise NameNotFoundError(ErrorStrings.Err_Id_Not_In_Collection.value.format(itemId))
        return item

    # This method gives a new key name to an already defined item.
    def _modifyNameInCollection(self, toFind: str, newName: str):
        item: T = self._retrieveFromCollection(toFind)

        # check that newName is unique to avoid data overwrites
        if newName in self.collection:
            raise DuplicateNameError(
                ErrorStrings.ERR_Not_Unique_Name.value.format(newName, item.getConfiguration().getIdField())
            )

        # modify configuration to reflect new name
        item.updateConfig({item.getConfiguration().getIdField(): newName})

        # update collection, make new key and delete the old one
        self.collection[newName] = self.collection[toFind]
        del self.collection[toFind]
