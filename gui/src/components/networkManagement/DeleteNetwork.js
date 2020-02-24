import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

const getAllNetworksBaseUrl = 'http://localhost:5000/chariot/api/v1.0/networks/names';
const deleteNetworkBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network';
const xhr = new XMLHttpRequest();

class DeleteNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworkNames: null,
      existingNetworkDescriptions: null,
      confirmIsOpen: false,
      selectedNetworkToDelete: null,
      successIsOpen: false
    }

    this.hideConfirmationModal = this.hideConfirmationModal.bind(this);
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
    }
    
    xhr.send();
  }

  // Create the links to settings for the gotten networks
  createNetworkLinks() {
    var networkLinks = [];
    
    // Go through all network names
    for (var i = 0; i < this.state.existingNetworkNames.length; i++) {
      var curNetwork = this.state.existingNetworkNames[i];

      // Create button links for every network so when user clicks on one, they can delete it
      networkLinks.push(
        <div key={i}>
          <Button id={curNetwork} variant="link" onClick={this.deleteConfirmation.bind(this, curNetwork)}>  
            {curNetwork}
          </Button>
        </div>
      );
    }

    return networkLinks;
  }

  deleteConfirmation(selectedNetwork) {
    this.setState({confirmIsOpen: true});
    this.setState({selectedNetworkToDelete: selectedNetwork});
  }

  hideConfirmationModal(event) {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault();
  }

  toggleSuccessModal = () => {
    xhr.open('DELETE', deleteNetworkBaseUrl + "?NetworkName=" + this.state.selectedNetworkToDelete);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
        this.setState({
          confirmIsOpen: false
        });
        this.setState({
          successIsOpen: !this.state.successIsOpen
        });      
      }
    }

    xhr.send();

  }


  render() {
    return [
      <div className="container" key="deleteNetworkScreen">
        <h1>Delete an Existing Network</h1>
        <p className="screenInfo">
          Select a network to delete. Deleting a network will also delete its corresponding devices.
        </p>

        {this.state.existingNetworkNames ? this.createNetworkLinks() : null}
        
        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="networkDeletionConfirmModal">
        <Modal.Body>
          To confirm the deletion of the network, {this.state.selectedNetworkToDelete}, click 'Yes'.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="networkDeletionSuccessModal">
        <Modal.Body>The network has been deleted!</Modal.Body>
        <Modal.Footer>
          <Link to="/welcome">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>
    ]
  }

}

export default DeleteNetwork; 