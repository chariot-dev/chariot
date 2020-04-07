import React, {Component} from 'react';
import { Table } from 'react-bootstrap';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';

import greenCircleImg from "../images/green_circle.png";
import yellowCircleImg from "../images/yellow_circle.png";
import redCircleImg from "../images/red_circle.png";

class DataCollectionEpisodeStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chosenNetwork: this.props.location.networkProps['Network Name'],
      networkDevices: this.props.location.networkProps['Devices'],
    }
  }

  getDeviceStatus(curDeviceName) {
    var networkName = this.state.chosenNetwork;

    // API CALL TO GET DEVICE STATUS ON THE NETWORK
    var deviceStatus = false;

    switch(deviceStatus) {
      case true:
        return <img src={greenCircleImg} alt="redCircleImage" className="deviceStatusImg"/>;
      case false:
        return <img src={redCircleImg} alt="redCircleImage" className="deviceStatusImg"/>;
      default:
        return <img src={redCircleImg} alt="redCircleImage" className="deviceStatusImg"/>;

    }
    
  }

  generateDevicesStatusTable() {
    var devicesTableElement = [];

    for (var i = 0; i < this.state.networkDevices.length; i++) {
      var curDeviceName = this.state.networkDevices[i];
      console.log(this.state.networkDevices[i]);

      // Create status row for current device. First cell is device name, second cell will use API call to determine device's status presently
      devicesTableElement.push(
        <tr key={curDeviceName + "StatusRow"}>
          <td>{curDeviceName}</td>
          <td> {this.getDeviceStatus(curDeviceName)} </td>
        </tr>
      );
    }

    return (
      <Table striped bordered>
        <thead>
          <tr>
            <th colSpan="2">{this.state.chosenNetwork}</th>
          </tr>
          <tr>
            <td>Device Name</td>
            <td>Device Status</td>
          </tr>
        </thead>
        <tbody>
          {devicesTableElement}
        </tbody>
      </Table>
    );
  }

  render() {
    return [
      <div className="container">
        <h1>Data Collection Episode</h1>
        <p>Data collection episode for {this.state.chosenNetwork}.</p>
        <div id="devicesCollectionStatus">
          {this.generateDevicesStatusTable()}
        
        </div>

        {/* Does nothing except go back to welcome screen for now */}
        <Link to={{pathname:'/welcome'}}>
          <Button variant="danger" className="float-right">End Data Collection</Button>
        </Link>

      </div>
    ]
  }
}

export default DataCollectionEpisodeStatus;