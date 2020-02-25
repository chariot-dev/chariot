/*
  The component handles the display of the screen to modify a network's network-specific properties.
*/

import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const getNetworkDetailsBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network';
const xhr = new XMLHttpRequest();

class ManageNetworkConfiguration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNetworkName: this.props.location.networkProps["Network Name"],
      originalNetworkProperties: {}, // Filled by componentDidMount()
      newNetworkProperties: {
        "Network Name": "",
        "Network Description": ""
      },
      confirmIsOpen: false,
      successIsOpen: false,
      errorIsOpen: false
    }    

    this.toggleConfirmationModal = this.toggleConfirmationModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }


  handleChange(event) {
    var updatedNetworkProperties = this.state.newNetworkProperties; // Store from current state
    updatedNetworkProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ newNetworkProperties: updatedNetworkProperties }); // Update the state
  }


  toggleConfirmationModal(event) {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
    });
    event.preventDefault();
  }


  // Gets run upon initial component render to load the default values of the text fields
  componentDidMount() {
    xhr.open('GET', getNetworkDetailsBaseUrl + '?NetworkName=' + this.state.originalNetworkName);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Once a response is received
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
        if (xhr.status === 200) {
          var responseJsonArray = JSON.parse(xhr.response); // Response is a dictionary 

          var properties = {};
          properties["Network Name"] = responseJsonArray["NetworkName"];
          properties["Network Description"] = responseJsonArray["Description"];

          this.setState({originalNetworkProperties: properties});

          // Initialize all to-be-saved properties to be the original, in the event not all properties are modified so can still be saved
          this.setState({newNetworkProperties: properties});
        }
      }
    }
    
    xhr.send();
  }


  updateNetworkConfiguration = () => {
    xhr.open('PUT', getNetworkDetailsBaseUrl);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    // Once a response is received
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
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
      "NetworkName": this.state.originalNetworkName,
      "NewName": this.state.newNetworkProperties["Network Name"],
      "Description": this.state.newNetworkProperties["Network Description"]
    }
    
    xhr.send(JSON.stringify(data));
  }


  render() {
    return [
      <div className="container" key="modifyNetworkNetworkSpecificSettingsScreen">
        <h1>{this.state.originalNetworkName} - Network Configuration</h1>
        <p className="screenInfo">Modify the network-specific configuration for {this.stateoriginalNetworkName} below, then click 'Save' to confirm the changes.</p>

        <form id="modifyNetworkForm" onSubmit={this.toggleConfirmationModal}>
            <div className="form-group">
              Network Name: <input className="form-control" id="networkNameInput" name="Network Name" defaultValue={this.state.originalNetworkName} onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              Network Description: <textarea className="form-control" id="networkDescriptionInput" rows="5" name="Network Description" defaultValue={this.state.originalNetworkProperties["Network Description"]} onChange={this.handleChange}></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button" type="submit">Save</Button>
        </form>

      </div>,

    <Modal show={this.state.confirmIsOpen} key="modifyNetworkNetworkSpecificSettingsConfirmationModal">
        <ConfirmationModalBody
          confirmationQuestion='Are the network settings displayed below correct?'
          confirmationData = {this.state.newNetworkProperties}
          >
        </ConfirmationModalBody>
        
      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.toggleConfirmationModal}>No</Button>
        <Button variant="primary" className="float-right" onClick={this.updateNetworkConfiguration}>Yes</Button>
      </Modal.Footer>
    </Modal>,

    <Modal show={this.state.successIsOpen} key="modifyNetworkNetworkSpecificSettingsSuccessModal">

      <SuccessModalBody successMessage='The network was succesfully modified! Click "Continue" to go back to the "Network Manager" screen.'>
      </SuccessModalBody>

      <Modal.Footer>
        <Link to="/networkManager">
          <Button variant="primary" className="float-left">Continue</Button>
        </Link>
      </Modal.Footer>
    </Modal>,

    <Modal show={this.state.errorIsOpen} key="modifyNetworkNetworkSpecificSettingsErrorModal">

      <ErrorModalBody errorMessage="The network could not be modified. Please go back, verify that the information is correct, and then try again.">
      </ErrorModalBody>

      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
      </Modal.Footer>
    </Modal>

    ]
  }
}

export default ManageNetworkConfiguration;