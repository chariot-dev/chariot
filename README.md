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

Navigate to the directory.

`$ cd path/to/chariot`

To install the Chariot core, run the `install-core.sh` script.

`$ bash install-core.sh`

To install the Chariot GUI, run the `install-gui.sh` script.

`$ bash install-gui.sh`

## Usage

To start the Chariot core, run the `run-core.sh` script.

`$ bash run-core.sh`

To start the Chariot GUI, run the `run-gui.sh` script.

`$ bash run-gui.sh`

TODO add instructions to make REST calls via curl, instructions to use GUI.

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
