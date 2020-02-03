from enum import Enum

class ErrorStrings(Enum):
    ERR_Specify_Identifier = 'Please specify a {} name in this request, %s'
    ERR_Not_Unique_Name = '{} is not a unique name for {}, %s, %s'
    ERR_Not_Found_In_Collection = 'The {} name {} has not been found in {}, %s, %s '
