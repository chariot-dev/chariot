from abc import ABC
from typing import Any, Dict
from typing import TypeVar
from chariot.utility.exceptions import NoIdentifierError, DuplicateNameError, NameNotFoundError, ErrorStrings

T = TypeVar('T')  # Declare type variable


class Manager(ABC):
    # this class will act as a base class for all manager classes. It will allow for management of items in a collection
    def __init__(self):
        self.collection: Dict[str, Any] = {}

    def _addToCollection(self, t: T) -> None:
        id: str = t.getConfiguration().getId()
        if id is None:
            raise NoIdentifierError(ErrorStrings.ERR_Specify_Network_Identifier)

        # When adding a key, if the same key is in the dict, the values are overriden. Avoid this.
        if id not in self.collection:
            self.collection[id] = t
        else:
            raise DuplicateNameError(ErrorStrings.ERR_Not_Unique_Network_Name.value.format(id))

    def _deleteFromCollection(self, id: str):
        if id is None:
            raise NoIdentifierError(ErrorStrings.ERR_Specify_Network_Identifier)

        if id in self.collection:
            del self.collection[id]
        else:
            raise NameNotFoundError(
                ErrorStrings.ERR_Network_Not_Found_In_Collection.value.format(id))

    # Convenience method used to return a generic object via a given network name
    def _retrieveFromCollection(self, id: str) -> T:
        try:
            t: T = self.collection[id]
        except KeyError:
            raise NameNotFoundError(
                ErrorStrings.ERR_Network_Not_Found_In_Collection.value.format(id))
        return t

    # This method gives a new key name to an already defined item.
    def _modifyNameInCollection(self, newName: str, toFind: str):
        # check that newName is unique to avoid data overwrites
        if newName in self.collection:
            raise DuplicateNameError(
                ErrorStrings.ERR_Not_Unique_Network_Name.value.format(newName)
            )

        t: T = self._retrieveFromCollection(toFind)

        t.getConfiguration().updateConfig({t.getConfiguration().getIdField(): newName})

        # update collection, make new key and delete the old one
        self.collection[newName] = self.collection[toFind]
        del self.collection[toFind]
