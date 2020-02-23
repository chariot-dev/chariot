/*
  AddNetwork.js

  This component the represents the screen where the user will initially configure the name
  and description of their network.

*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const postCreateNetworkBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network';
const xhr = new XMLHttpRequest();

class AddNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      networkProperties: {
        "Network Name": "",
        "Network Description": ""
      },
      isSubmitted: false,
      confirmIsOpen: false,
      successIsOpen: false,
      errorIsOpen: false
    }

    this.handleNetworkAdd = this.handleNetworkAdd.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleNetworkAdd(event) {
    this.setState({ isSubmitted: true });
    event.preventDefault();
  }
  
  handleChange(event) {
    var updatedNetworkProperties = this.state.networkProperties; // Store from current state
    updatedNetworkProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ networkProperties: updatedNetworkProperties }); // Update the state
  }

  toggleConfirmationModal = () => {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
    });
  }

  toggleErrorModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      errorIsOpen: !this.state.errorIsOpen
    });
  }

  createNetworkAndToggleSuccessModal = () => {
    xhr.open('POST', postCreateNetworkBaseUrl);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = () => { // Call a function when the state changes.
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          this.setState({
            confirmIsOpen: false
          });
          this.setState({
            successIsOpen: !this.state.successIsOpen
          });
        }
        else {
          this.setState({ errorIsOpen: !this.state.errorIsOpen });
        }
      }
    }

    var data = {
      "NetworkName": this.state.networkProperties["Network Name"], 
      "Description": this.state.networkProperties["Network Description"]
    }

    xhr.send(JSON.stringify(data));
  }

  render() {
    return [
      <div className="container" key="addNetworkForm">
        <h1>Add a New Network</h1>
          <p className="screenInfo">Please fill in the fields below to create a network. Then, click "Next".</p>
          
          <form id="createNetworkForm" onSubmit={this.handleNetworkAdd}>
            <div className="form-group">
              <input className="form-control" id="networkNameInput" name="Network Name" placeholder="Network Name" onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="networkDescriptionInput" rows="5" name="Network Description" placeholder="Network Description" onChange={this.handleChange}></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button" onClick={this.toggleConfirmationModal}>Next</Button>
        </form>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="addNetworkConfirmation">
          <ConfirmationModalBody
            confirmationQuestion='Is this information for your network correct?'
            confirmationData = {this.state.networkProperties}
            >
          </ConfirmationModalBody>
          
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleConfirmationModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.createNetworkAndToggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="addNetworkSuccessModal">

        <SuccessModalBody successMessage="Your network was succesfully added! Would you like to add a device to this network as well?">
        </SuccessModalBody>

        <Modal.Footer>
          <Link to="/networkManager">
            <Button variant="primary" className="float-left">No</Button>
          </Link>
          <Link to={{pathname:'/addDeviceHome', networkProps:{'Network Name': this.state.networkProperties['Network Name']} }}>
            <Button variant="primary" className="float-right">Yes</Button>
          </Link>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.errorIsOpen} key="addNetworkErrorModal">

        <ErrorModalBody errorMessage="Your network was not created. Please go back, verify that the information is correct, and then try again.">
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>
    ]
  }

}

export default AddNetwork; 