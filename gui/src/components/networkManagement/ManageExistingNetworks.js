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
import BaseURL from "../utility/BaseURL";

const getAllNetworksBaseUrl = BaseURL + 'networks/all';

class ManageExistingNetworks extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworks: []
    }
  } 




  componentDidMount() {
    // Execute the get request to 'getAllNetworksBaseUrl' using fetch
    fetch(getAllNetworksBaseUrl)
    .then(res => res.json())
    .then(
      // If get was successful, update state with recieved network information
      (result) => {
        console.log(result);
        var responseJsonArray = result;
        
        var updatedNetworksJsonArray = this.state.existingNetworks; 
        for (var i = 0; i < responseJsonArray.length; i++) {
          updatedNetworksJsonArray.push(responseJsonArray[i]);
        }


        this.setState({ existingNetworks: updatedNetworksJsonArray });
      },  
      
      /*
        If get was unsuccessful, update state and display error modal
      */
      (error) => {
        console.log(error.message);
      }
    )
  }
  


  render() {
    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <p className="screenInfo">
          Select a network to modify its existing configuration settings. Select a device under a network to modify the device's existing configuration settings.
        </p>
        
        {/* {this.state.existingNetworks ? this.createNetworkLinks() : null} */}
        {this.state.existingNetworks.length > 0 ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingNetworks} withLinks={true} type="manage"></NetworkDeviceCellScreenTemplate> : <p>No existing networks were found.</p>}


        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button> 
        </Link>
      </div>
    );
  }




}


export default ManageExistingNetworks;
