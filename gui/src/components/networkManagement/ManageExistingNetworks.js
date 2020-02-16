import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const getAllNetworksBaseUrl = 'http://localhost:5000/chariot/api/v1.0/networks/names';
const xhr = new XMLHttpRequest();

class ManageExistingNetworks extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworkNames: null,
      existingNetworkDescriptions: null
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
        var responseJson = JSON.parse(xhr.responseText); // Response is a dictionary 
        
        // Getting network names/descriptions and adding them to respective arrays
        var tempNetworkNames = [];
        var tempNetworkDescriptions = [];
        for (var networkName in responseJson) {
          tempNetworkNames.push(networkName);
          tempNetworkDescriptions.push(responseJson[networkName]);
        }
        
        // Update state with gotten network names and descriptions
        this.setState({existingNetworkNames: tempNetworkNames});
        this.setState({existingNetworkDescriptions: tempNetworkDescriptions});
      }
    }
    
    xhr.send();
  }

  // Create the links to settings for the gotten networks
  createNetworkLinks() {
    var networkLinks = [];

    for (var i = 0; i < this.state.existingNetworkNames.length; i++) {
      var curNetwork = this.state.existingNetworkNames[i];

      networkLinks.push(
        <div key={i}>
          <Link className="link" to={"/" + curNetwork + "/settings"}>{curNetwork}</Link><br></br>
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
        <p className="screenInfo">Select a network to modify its existing configuration settings.</p>
        
        {this.state.existingNetworkNames ? this.createNetworkLinks() : null}

        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button> 
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 