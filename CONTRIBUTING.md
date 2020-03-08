# Contributing to Chariot

## Introduction

This document serves as the reference for developers who would like to get the development environment setup and understand the intended workflow required to contribute to this project. This is still a work in progress as the project evolves.

## Setting up the dev environment

The development environment can be setup using the `install.sh` script found in the `/install` directory. Further information on setting up the environment can be found in the [README.md](README.md) file.

## Package structure

Chariot's backend is implemented as a Python package. The top-level module is located at `chariot/src/chariot`.

### Running core modules

The system core is structured as a Python package. You may run individual modules using the format

`python3 -m chariot.network.Network`

(note, no `.py` extension)

### Importing modules

To import one Chariot submodule into another please follow the style used in existing modules.
For example lests look at the imports in `chariot/src/chariot/device/adapter/ImpinjR420Adapter.py`:
```
from chariot.utility.JSONTypes import JSONObject
from chariot.device.adapter import DeviceAdapter
from chariot.device.configuration import ImpinjR420Configuration
```
This submodule imports:
* The `JSONObject` constant from the submodule `chariot/src/chariot/JSONTypes.py`
* The `DeviceAdapter` class from the submodule `chariot/src/chariot/device/adapter/DeviceAdapter.py`
* The `ImpinjR420Configuration` class from the submodule `chariot/src/chariot/device/configuration/ImpinjR420Configuration.py`

To allow new modules to use this importing style the full module must be imported to the local `__init__.py`. 

## Development Practices

Chariot is developed with the idea of interchangeable modules that conform to the expected APIs defined by a parent module. Any new modules must be located with other similar modules and not interfere with the function of existing modules.
If a change must be made across multiple modules this change should be properly documented so others are aware of how to use it.

### Pushing changes

Chariot follows a Pull Request model in that all changes to the master branch must be merged from a pull request. In the future, the project will have integrated CI which must pass for changes to be accepted. In the meantime, it is paramount to ensure all `tox` checks are passing before creating a pull request.
