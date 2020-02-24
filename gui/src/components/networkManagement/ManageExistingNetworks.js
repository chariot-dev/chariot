import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const getAllNetworksBaseUrl = 'http://localhost:5000/chariot/api/v1.0/networks/all';
const xhr = new XMLHttpRequest();

class ManageExistingNetworks extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworks: []
    }
  } 


  componentDidMount() {
    this.getExistingNetworks();
  }

  getExistingNetworks = () => {
    xhr.open('GET', getAllNetworksBaseUrl);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Once a response is received
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
        if (xhr.status === 200) {
          var responseJsonArray = JSON.parse(xhr.response); // Response is a dictionary 

          var updatedNetworksJsonArray = this.state.existingNetworks; 

          for (var i = 0; i < responseJsonArray.length; i++) {
            updatedNetworksJsonArray.push(responseJsonArray[i]);
          }

          this.setState({ existingNetworks: updatedNetworksJsonArray });
        }
      }
    }
    
    xhr.send();
  }

  // Create the links to settings for the gotten networks
  createNetworkLinks() {
    var networkLinks = [];
    
    for (var i = 0; i < this.state.existingNetworks.length; i++) {
      var deviceLinks = []; // Reset list of devices for network-to-be-displayed
      var curNetworkName = this.state.existingNetworks[i]["NetworkName"];
      var curNetworkDescription = this.state.existingNetworks[i]["Description"];
   
      // Now create links for network's corresponding devices
      for (var k = 0; k < this.state.existingNetworks[i]["Devices"].length; k++) {
        var curDeviceKey = curNetworkName + "Device" + k;
        var curDeviceName = this.state.existingNetworks[i]["Devices"][k];
        
        deviceLinks.push(
          <div key={curDeviceKey} className="networksDeviceLink">
            <b>Device {k + 1}: </b>
              <Link to={{pathname:"/manageExistingDevice/" + curNetworkName + "/" + curDeviceName, deviceProps:{'Network Name': curNetworkName, 'Device Name': curDeviceName} }}>
                {curDeviceName}
              </Link><br></br>
          </div>
        );
      }      

      networkLinks.push(
        <div className="existingNetworkBox" key={i}>
          <div className="existingNetworkCell">
            <Link to={{pathname:'/addDeviceHome', networkProps:{'Network Name': curNetworkName}}}> 
              <Button className="float-right" variant="light" size="sm">Add Device</Button>
            </Link>
            
            <div>
              <b>Network Name: </b> 
                <Link to={{pathname:"/manageExistingNetwork/" + curNetworkName, networkProps:{'Network Name': curNetworkName} }}>
                  {curNetworkName}
                </Link><br></br>
              <b>Description: </b> {curNetworkDescription}<br></br>
            </div>
            {deviceLinks}
          </div>
        </div>
      );
    }

    return networkLinks;
  }

  render() {

    // ================================= Need a robust way of mapping the paths to network settings since they're all dynamic =================================
    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <p className="screenInfo">
          Select a network to modify its existing configuration settings. Select a device under a network to modify the device's existing configuration settings.
        </p>
        
        {this.state.existingNetworks ? this.createNetworkLinks() : null}

        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button> 
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 