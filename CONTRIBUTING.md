# Contributing to Chariot

## Introduction

This document serves as the reference for developers who would like to get the development environment setup and understand the intended workflow required to contribute to this project. This is still a work in progress as the project evolves.

## Setting up the dev environment

These instructions are split into those for the official [front-end](#setting-up-the-front-end) and the [core](#setting-up-the-core), since the core works independent of the front-end and exposes a REST-ful API which enables any developer to write their own front-end.

### Setting up the core
The entirety of the core is written in Python. Thus the following are required in order to have a working dev environment:
* NIX\* environment (Linux, WSL, macOS terminal)
* [Python](https://github.com/python/cpython) (3.5 and above)
* [pip](https://github.com/pypa/pip)

Keep in mind that we enforce the use of python3 type hints as much as possible, to avoid obscurity.

Follow these steps to finish setting up:
```
(Within chariot/src)
(Create and activate a new virtual environment)
$ python3 -m venv .
$ source ./bin/activate

(Install dependencies)
$ pip install -r requirements.txt

(Run linters, typechecks and tests)
$ tox
```
If all tests have passed, you are ready to start contributing.

### Setting up the GUI
As the Core and GUI of Chariot are separated a developer could create their own GUI environment, but to contribute to the official Chariot GUI they will need the following to have a working dev environment:

* [Node.js](https://github.com/nodejs/node) (v12.x +)
* [Yarn](https://github.com/yarnpkg/yarn)
* [Electron](https://github.com/electron/electron)

The core environment is required as all logic and tasks are finally completed within the core.

Follow these steps to finish setting up the GUI environment:
```
(Within chariot/gui)
$ yarn install
```
Afterwards you should now be able to start the GUI alongside the core and begin GUI development.

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
