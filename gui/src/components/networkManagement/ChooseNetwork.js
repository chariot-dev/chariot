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

import BaseURL from "../utility/BaseURL";

const getAllNetworksBaseUrl = BaseURL + 'networks/all';
const xhr = new XMLHttpRequest();

class ChooseNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworks: []
    }
  }

  componentDidMount () {
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

  render() {
    console.log(this.state.existingNetworks);

    return (
      <div className="container">
        <h1>Choose a Network</h1>
        <p className="screenInfo">
          Select a network to begin data collection process.
        </p>

        {this.state.existingNetworks ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingNetworks} withLinks={false} type="choose"></NetworkDeviceCellScreenTemplate> : null}

        <Link to="/welcome">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork;
