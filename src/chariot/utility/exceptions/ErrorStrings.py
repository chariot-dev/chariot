from enum import Enum


class ErrorStrings(Enum):
    ERR_Specify_Network_Identifier = 'Please specify a Network name in this request'
    ERR_Specify_Device_Identifier = 'Please specify a device name in this request'
    ERR_Not_Unique_Device_Name = '{0} is not a unique device name in {1}.'
    ERR_Not_Unique_Network_Name = '{0} is not a unique network name.'
    ERR_Device_Not_Found_In_Collection = 'The device "{0}" has not been found in {1}.'
    ERR_Network_Not_Found_In_Collection = 'The network name "{0}" does not exist.'
    ERR_Device_Not_Supported = 'The device type given is not supported by Chariot'
    ERR_Generic_Device_Template = 'Could not open file /device/drive/GenericRequiredFields.json'
