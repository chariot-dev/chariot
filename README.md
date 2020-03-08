# Chariot
The Internet of Things (IoT) is a system of connected devices capable of collecting and transferring data. Different users of IoT devices may be interested in different types of data. A gardener might want to track the pH value of their soil and the air humidity. A city planner may look for a way to track pedestrian traffic in common spaces. A factory manager might look for a way to track the status of machinery and production rates.

IoT infrastructure has exploded in the past decade, so there are devices on the market to collect data for a wide variety of applications. But the wide variety of devices requires special considerations. A Wi-Fi 4K camera connects to a network much differently than a home thermometer. A motion detector may collect and transfer data in a different form than a pressure sensor.

So, despite progress in the IoT industry, it is still difficult to integrate different types of devices into a unified system. Chariot solves this problem. Chariot is a platform for IoT device management, data storage, and analysis. Users can add, remove, and configure a variety of devices on a single network. With Chariot, a gardener could purchase a pH and humidity IoT devices off the shelf and gather data from his soil and the air from one convenient interface.

## Table of Contents
- [Features](##Features)
- [Getting Started](##Getting-Started)
- [Usage](##Usage)
- [Contributing](##Contributing)
- [License](##License)
- [Contributors](##Contributors)
- [Acknowledgments](##Acknowledgments)

## Features

Chariot offers:
- A platform to use heterogeneous IoT devices regardless of device protocols,
- Drop in, drop out device connection,
- Connection to powerful database engines,
- Modular addition of device adapters to expand Chariot's capabilities.

## Getting Started

### Prerequisites

The Chariot core exposes a REST-ful API to manage devices, networks, and database connections. The following are required to set up and run the Chariot core:

- A *nix environment,
- Python 3.5+,
- pip,
- The [venv](https://docs.python.org/3/library/venv.html) Python module.

The Chariot GUI interfaces with the core API. The following are required to set up and run the Chariot GUI:

- Node.js (v12.x +),
- [Yarn](https://yarnpkg.com/).

### Installation

Use the *nix shell to install. Start by cloning this repository.

`$ git clone https://github.com/chariot-dev/chariot.git`

Navigate to the `install` directory.

`$ cd path/to/chariot/install`

To install both Chariot's core and GUI, run the `install.sh` script.

`$ bash install.sh`

To install just Chariot core, run the `install-core.sh` script.

`$ bash install-core.sh`

To install the Chariot GUI, run the `install-gui.sh` script.

`$ bash install-gui.sh`

### Usage

#### Starting Chariot

To start Chariot's webserver and utilize its backend, navigate to the `run` directory and run the `run-core.sh` script.

`$ cd path/to/chariot/run`
`$ bash run-core.sh`

To start the Chariot GUI, run the `run-gui.sh` script.
This will attempt to connect to the local server, and must be performed after it is started.

`$ bash run-gui.sh`

To run the core and the GUI in a single command, run the `run.sh` script.

#### CLI
Chariot's server can be accessed via a terminal environment using utilities like curl.
Below is an example usage to create a new network, add a device, and review that network and its device configurations.

```
(Creating a new network)
$ curl -i -X POST localhost:5000/chariot/api/v1.0/network -H "content-Type: application/json" -d '{"networkName":"test", "description":"this is my test network"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 22
Access-Control-Allow-Origin: *
Server: Werkzeug/0.16.0 Python/3.8.1
Date: *Current Date and Time*

{
    "success": true
}

(Adding a device to a network)
(Notice that the associated network must be specified by the `networkName` field.)
$ curl -i -X POST localhost:5000/chariot/api/v1.0/network/device -H "content-Type: application/json" -d '{"networkName":"test", "deviceID":"MyDevice", "deviceType":"Device", "ipAddress":"IP Address", "pollDelay":3, *Device Specific Configurations*}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 22
Access-Control-Allow-Origin: *
Server: Werkzeug/0.16.0 Python/3.8.1
Date: *Current Date and Time*

{
    "success": true
}
```
Thanks to running as a web server, all endpoints can be accessed with curl commands like those demonstrated above.
For documentation of all API endpoints please see the [API_ENDPOINTS.md](API_ENDPOINTS.md) file.

#### GUI
All of Chariot's features can be utilitized through the GUI. This is an alternative to using the CLI.
The features that are currently functioning are:
* Creating a network
* Creating a device
* Deleting a network
* Deleting a device from a network
* Modifying a network's properties (a little buggy)

The features that are not fully functioning are:
* Authentication (creating an account and logging in with said account)
* Adding another device to existing network (a little buggy)
* Connecting to database to configure data collection
* Data collection from device
* Modifying a device (a little buggy)
* Monitoring device status as data collection episode is in progress
* Performing data analysis

## Contributing

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for instructions on how to set up a development environment and contribute to Chariot.

## License

This project is licensed under the GNU Lesser General Public License v3.0. See the [LICENSE.md](LICENSE.md) file for details.

## Contributors
* [Enioluwa Segun](https://github.com/enioluwa23)
* [Ryan Hassing](https://github.com/ryanhassing)
* [Juan Garcia-Lopez](https://github.com/Juan-Garcia96)
* [John Ho](https://github.com/jh3377)
* [Medard Azandegbe](https://github.com/maa433)
* [Kamalludin Colaire](https://github.com/kac486)
* [Christopher Mak](https://github.com/auronsento)

## Acknowledgments
The team would like to thank:

* [Dr. Bill Mongan](http://www.billmongan.com/), for his guidance, as well as for the [IoT Framework](http://www.billmongan.com/portfolio/iotframework/) source code,
* Dr. Dandekar and Dr. Pano at the [Drexel Wireless Systems Laboratory](https://research.coe.drexel.edu/ece/dwsl/), for their guidance and the use of their facilities,
* Dr. Hislop, our Senior Design advisor, for his support and guidance.
