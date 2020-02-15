from enum import Enum


class ErrorStrings(Enum):
    ERR_Specify_Identifier = 'Please specify a {} name in this request, %s'
    ERR_Not_Unique_Name = '{0} is not a unique name in this context'
    ERR_Not_Found_In_Collection = 'The {0} name {1} has not been found in {2}'
