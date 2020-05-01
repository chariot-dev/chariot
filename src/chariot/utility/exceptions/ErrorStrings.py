from enum import Enum


class ErrorStrings(Enum):
    ERR_Specify_Identifier = 'Please specify a {} in this request'
    ERR_Not_Unique_Name = '{0} is not a unique {1} in this collection.'
    Err_Id_Not_In_Collection = '{} has not been found in this collection'
    ERR_Item_Not_Supported = 'The {0} type {1} is not supported by Chariot'
    ERR_Generic_Device_Template = 'Could not open file {0}'
    Err_General_Id = 'id'
    ERR_Login_Failed = 'The credentials are invalid'
