/*


*/

import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

class NetworkDeviceCellScreenTemplate extends Component {
  constructor(props) {
    super(props);
    this.state = {
      dataJson: this.props.dataJson,
      withLinks: this.props.withLinks, // withLinks = true means clicking on network/devices is possible
      type: this.props.type // manage, delete, choose
    }
  }


  createCells = () => {
    var networkLinks = [];

    for (var i = 0; i < this.state.dataJson.length; i++) {
      var deviceTags = []; // Reset list of devices for network-to-be-displayed
      var curNetworkName = this.state.dataJson[i]["NetworkName"];
      var curNetworkDevices = this.state.dataJson[i]["Devices"];
      var curNetworkDescription = this.state.dataJson[i]["Description"];

      var buttonElement = [];

      switch (this.state.type) {
        // For DeleteNetwork
        case "delete":
          buttonElement.push(
            <Button key={"deleteNetworkButton" + i} className="float-right" variant="danger" size="sm" onClick={this.props.deleteNetwork.bind(this, curNetworkName)}>
              Delete Network
            </Button>
          )            
          break;
        // For ManageExistingNetworks
        case "manage":
          buttonElement.push(
            <Link key={"manageNetworkButton" + i} to={{pathname:'/addDeviceHome', networkProps:{'Network Name': curNetworkName}}}> 
              <Button className="float-right" variant="light" size="sm">
                Add Device
              </Button>
            </Link>
          )
          break;
        // For ChooseNetwork
        case "choose":
          buttonElement.push(
            <Link key={"chooseNetworkButton" + i} to={{pathname:'/databaseConnection', networkProps:{'Network Name': curNetworkName, 'Devices': curNetworkDevices}}}> 
              <Button className="float-right" variant="success" size="sm">
                Choose Network
              </Button>
            </Link>
          )
          break;
        default:
          buttonElement.push(undefined);
      }
      
      if (this.state.withLinks) {
        var curDeviceKey;
        var curDeviceName;

        // Create links for network's corresponding devices
        if (this.state.dataJson[i]["Devices"].length > 0) {
          for (var k = 0; k < this.state.dataJson[i]["Devices"].length; k++) {
            curDeviceKey = curNetworkName + "Device" + k;
            curDeviceName = this.state.dataJson[i]["Devices"][k];       
            deviceTags.push(
              <div key={curDeviceKey} className="networksDeviceLink">
                <b>Device {k + 1}: </b>
                  <Link to={{pathname:"/manageExistingDevices/devices/" + curNetworkName + "/" + curDeviceName, networkProps:{'Network Name': curNetworkName, 'Device Name': curDeviceName} }}>
                    {curDeviceName}
                  </Link><br></br>
              </div>
            );
          }
        }
        // If now devices, say so
        else {
          deviceTags.push(
            <div key="noDevices" className="networksDeviceLink">
              No devices exist for this network.
            </div>
          );
        }

        // Create links for network, then create the jsx for networks/devices
        networkLinks.push(
          <div className="existingNetworkBox" key={i}>
            <div className="existingNetworkCell">

              {buttonElement}
              
              <div>
                <b>Network Name: </b> 
                  <Link to={{pathname:"/manageExistingNetwork/" + curNetworkName, networkProps:{'Network Name': curNetworkName} }}>
                    {curNetworkName}
                  </Link><br></br>
                <b>Description: </b> {curNetworkDescription}<br></br>
              </div>
              {deviceTags}
            </div>
          </div>
        );
      }
      else { // without links
        if (this.state.dataJson[i]["Devices"].length > 0) {
          for (var j = 0; j < this.state.dataJson[i]["Devices"].length; j++) {
            curDeviceKey = curNetworkName + "Device" + j;
            curDeviceName = this.state.dataJson[i]["Devices"][j];       
            deviceTags.push(
              <div key={curDeviceKey} className="networksDeviceLink">
                <b>Device {j + 1}: </b>{curDeviceName}<br></br>
              </div>
            );
          }
        }
        // If now devices, say so
        else {
          deviceTags.push(
            <div key={curDeviceKey} className="networksDeviceLink">
              No devices exist for this network.
            </div>
          );
        }
        // Create links for network, then create the jsx for networks/devices
        networkLinks.push(
          <div className="existingNetworkBox" key={i}>
            <div className="existingNetworkCell">

              {buttonElement}
              
              <div>
                <b>Network Name: </b> {curNetworkName}<br></br>
                <b>Description: </b> {curNetworkDescription}<br></br>
              </div>
              {deviceTags}
            </div>
          </div>
        );

      }

    }


    return networkLinks;
  }


  render() {
    return (
      <div id="networkDeviceCells">
        {this.createCells()}
      </div>
    );
  }
}

export default NetworkDeviceCellScreenTemplate; 