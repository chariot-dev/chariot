# Package structure

The Chariot backend is implemented as a Python package. The top-level module is located at `chariot/src/chariot`.

## Running a module

Suppose you want to run a submodule within the Chariot backend package - for example, `chariot/src/chariot/core/network/Network.py`. To do so:

* Navigate to `chariot/src`.
* Run the command `python3 -m chariot.core.network.Network`. Note
	* The `-m` option, to run the code as a module,
	* Slashes are replaced with dots,
	* No `.py` extension.

## Importing a module

Suppose that you want to import one Chariot submodule into another. For example, let's look at the imports in `chariot/src/chariot/core/device/adapter/ImpinjR420Adapter.py`:

`from chariot.core.JSONTypes import JSONObject`
`from chariot.core.device.adapter.DeviceAdapter import DeviceAdapter`
`from chariot.core.device.configuration.ImpinjR420Configuration import ImpinjR420Configuration`

This submodule imports:

* The `JSONObject` constant from the submodule `chariot/src/chariot/core/JSONTypes.py`,
* The `DeviceAdapter` class from the submodule `chariot/src/chariot/core/device/adapter/DeviceAdapter.py`, and
* The `ImpinjR420Configuration` class from the submodule `chariot/src/chariot/core/device/configuration/ImpinjR420Configuration.py`.

Follow this format for correct imports.
