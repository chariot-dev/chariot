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
      errorIsOpen: false,
      errorMessage: ''
    }

    this.toggleConfirmationModal = this.toggleConfirmationModal.bind(this);
    this.hideConfirmationModal = this.hideConfirmationModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }
  
  handleChange(event) {
    var updatedNetworkProperties = this.state.networkProperties; // Store from current state
    updatedNetworkProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ networkProperties: updatedNetworkProperties }); // Update the state
  }

  toggleConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen });
    event.preventDefault();
  }

  hideConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen });   
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
    // Post request's body
    var data = {
      "networkName": this.state.networkProperties["Network Name"],
      "description": this.state.networkProperties["Network Description"]
    }

    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
    fetch(postCreateNetworkBaseUrl, requestOptions)
    .then(res => res.json())
    .then(
      // If post was successful, update state and display success modal
      () => {
        this.setState({
          confirmIsOpen: false
        });
        this.setState({
          successIsOpen: !this.state.successIsOpen
        });
      },
      // If post was unsuccessful, update state and display error modal
      (error) => {
        // Once error message is set, then launch the error modal
        this.setState({
          errorMessage: error.message 
        }, () => {
          this.setState({ errorIsOpen: !this.state.errorIsOpen });
        });
      }
    )
  }

  render() {
    return [
      <div className="container" key="addNetworkForm">
        <h1>Add a New Network</h1>
          <p className="screenInfo">Please fill in the fields below to create a network. Then, click "Next".</p>
          
          <form id="createNetworkForm" onSubmit={this.toggleConfirmationModal}>
            <div className="form-group">
              <div className="requiredStar">*</div>
              Network Name: <input required className="form-control" id="networkNameInput" name="Network Name" onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              <div className="requiredStar">*</div>
              Network Description: <textarea required className="form-control" id="networkDescriptionInput" rows="5" name="Network Description" onChange={this.handleChange}></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button" type="submit">Next</Button>
        </form>
      </div>,

      <Modal show={this.state.confirmIsOpen} onHide={this.hideConfirmationModal} key="addNetworkConfirmation">
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
          <Link to={{ pathname:'/addDeviceHome', networkProps:{'Network Name': this.state.networkProperties['Network Name']} }}>
            <Button variant="primary" className="float-right">Yes</Button>
          </Link>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.errorIsOpen} key="addNetworkErrorModal">
        <ErrorModalBody errorMessage={this.state.errorMessage + ". Please ensure that the server is running, the inputted values are valid, and try again." }>
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>
    ]
  }

}

export default AddNetwork; 