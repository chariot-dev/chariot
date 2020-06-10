/*
  This component handles the user having to choose a network to run the data collection episode on.
  The body of the screen (network/device info) is generated through the NetworkDeviceCellScreenTemplate 
  child component. Since the buttons in this component links the user to other components, a callback 
  to update this component's state isn't necessary. 

*/

import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

const getAllNetworksBaseUrl = 'http://localhost:5000/chariot/api/v1.0/networks/all';

class ChooseNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworks: []
    }
  }

  componentDidMount () {
    fetch(getAllNetworksBaseUrl)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var responseJsonArray = result;  

        var updatedNetworksJsonArray = this.state.existingNetworks;
        
        for (var i = 0; i < responseJsonArray.length; i++) {
          updatedNetworksJsonArray.push(responseJsonArray[i]);
        }

        this.setState({ existingNetworks: updatedNetworksJsonArray });
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }

  render() {
    return (
      <div className="container">
        <h1>Choose a Network</h1>
        <p className="screenInfo">
          Select a network that has devices to begin data collection process.
        </p>

        {this.state.existingNetworks ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingNetworks} withLinks={false} type="chooseNetwork"></NetworkDeviceCellScreenTemplate> : <p>No existing networks were found.</p>}

        <Link to="/welcome">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork; 