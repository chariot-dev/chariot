/*
  The component handles the functionality on the screen "Manage Existing Networks". The body of the screen 
  (network/device info) is generated through the NetworkDeviceCellScreenTemplate child component. Since the
  links and buttons in this component links the user to other components, a callback to update this component's
  state isn't necessary. 
*/


import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

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
          console.log(updatedNetworksJsonArray);
        }
      }
    }
    
    xhr.send();
  }
  

  render() {
    console.log(this.state.existingNetworks);

    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <p className="screenInfo">
          Select a network to modify its existing configuration settings. Select a device under a network to modify the device's existing configuration settings.
        </p>
        
        {/* {this.state.existingNetworks ? this.createNetworkLinks() : null} */}
        {this.state.existingNetworks ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingNetworks} withLinks={true} type="manage"></NetworkDeviceCellScreenTemplate> : null}

        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button> 
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 